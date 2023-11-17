import unittest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np
import engine
import json
from engine import get_recommendations, sp_login


class TestSpotifyFunctions(unittest.TestCase):
    @patch('spotipy.Spotify')
    def test_get_recent_tracks(self, mock_spotify):
        sp_instance = mock_spotify.return_value
        sp_instance.current_user_recently_played.return_value = {'items': [{'track': {'id': '123'}}, {'track': {'id': '456'}}], 'next': None}

        tracks, dates = engine.get_recent_tracks(sp_instance, 2)

        self.assertEqual(tracks, ['123', '456'])
        self.assertTrue(all(isinstance(date, str) for date in dates))

    @patch('spotipy.Spotify')
    def test_get_tracks(self, mock_spotify):
        sp_instance = mock_spotify.return_value
        sp_instance.track.return_value = {'name': 'Test Track'}

        track_info = engine.get_tracks(sp_instance, '123')

        self.assertEqual(track_info['name'], 'Test Track')

    def test_get_tracks_id(self):
        tracks = [{'track': {'id': '123'}}, {'track': {'id': '456'}}]
        track_ids = engine.get_tracks_id(tracks)

        self.assertEqual(track_ids, ['123', '456'])

    def test_get_date_played(self):
        tracks = [{'played_at': '2022-01-01'}, {'played_at': '2022-01-02'}]
        dates_played = engine.get_date_played(tracks)

        self.assertEqual(dates_played, ['2022-01-01', '2022-01-02'])

    @patch('spotipy.Spotify')
    def test_get_audio_features(self, mock_spotify):
        sp_instance = mock_spotify.return_value
        sp_instance.audio_features.return_value = [{'acousticness': 0.5, 'danceability': 0.7}]

        audio_features = engine.get_audio_features(sp_instance, ['123'])

        self.assertEqual(audio_features, [{'acousticness': 0.5, 'danceability': 0.7}])

    def test_get_recommendations(self):
        recommendations = get_recommendations(sp_login, "testdata/userdata_test.db", "testdata/recommendation_test.csv")
        my_str = ("{'album': {'album_type': 'album', 'artists': [{'external_urls': {'spotify': "
                  "'https://open.spotify.com/artist/3BiJGZsyX9sJchTqcSA7Su'}, 'href': "
                  "'https://api.spotify.com/v1/artists/3BiJGZsyX9sJchTqcSA7Su', 'id': '3BiJGZsyX9sJchTqcSA7Su', "
                  "'name': 'Dick Haymes', 'type': 'artist', 'uri': 'spotify:artist:3BiJGZsyX9sJchTqcSA7Su'}], "
                  "'available_markets': ['AR', 'AU', 'AT', 'BE', 'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', "
                  "'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', 'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', "
                  "'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', 'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', "
                  "'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', 'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', "
                  "'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', 'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', "
                  "'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', 'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', "
                  "'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', 'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', "
                  "'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', 'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', "
                  "'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'WS', 'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', "
                  "'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', 'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', "
                  "'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', 'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', "
                  "'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', 'TJ', 'VE', 'ET', 'XK'], 'external_urls': {"
                  "'spotify': 'https://open.spotify.com/album/3jYbgerYWz3j5AaazIf5qS'}, "
                  "'href': 'https://api.spotify.com/v1/albums/3jYbgerYWz3j5AaazIf5qS', "
                  "'id': '3jYbgerYWz3j5AaazIf5qS', 'images': [{'height': 640, "
                  "'url': 'https://i.scdn.co/image/ab67616d0000b2731367e2af0bb7790300a4798e', 'width': 640}, "
                  "{'height': 300, 'url': 'https://i.scdn.co/image/ab67616d00001e021367e2af0bb7790300a4798e', "
                  "'width': 300}, {'height': 64, 'url': "
                  "'https://i.scdn.co/image/ab67616d000048511367e2af0bb7790300a4798e', 'width': 64}], 'name': 'Dick "
                  "Haymes', 'release_date': '1922', 'release_date_precision': 'year', 'total_tracks': 20, "
                  "'type': 'album', 'uri': 'spotify:album:3jYbgerYWz3j5AaazIf5qS'}, 'artists': [{'external_urls': {"
                  "'spotify': 'https://open.spotify.com/artist/3BiJGZsyX9sJchTqcSA7Su'}, "
                  "'href': 'https://api.spotify.com/v1/artists/3BiJGZsyX9sJchTqcSA7Su', "
                  "'id': '3BiJGZsyX9sJchTqcSA7Su', 'name': 'Dick Haymes', 'type': 'artist', "
                  "'uri': 'spotify:artist:3BiJGZsyX9sJchTqcSA7Su'}], 'available_markets': ['AR', 'AU', 'AT', 'BE', "
                  "'BO', 'BR', 'BG', 'CA', 'CL', 'CO', 'CR', 'CY', 'CZ', 'DK', 'DO', 'DE', 'EC', 'EE', 'SV', 'FI', "
                  "'FR', 'GR', 'GT', 'HN', 'HK', 'HU', 'IS', 'IE', 'IT', 'LV', 'LT', 'LU', 'MY', 'MT', 'MX', 'NL', "
                  "'NZ', 'NI', 'NO', 'PA', 'PY', 'PE', 'PH', 'PL', 'PT', 'SG', 'SK', 'ES', 'SE', 'CH', 'TW', 'TR', "
                  "'UY', 'US', 'GB', 'AD', 'LI', 'MC', 'ID', 'JP', 'TH', 'VN', 'RO', 'IL', 'ZA', 'SA', 'AE', 'BH', "
                  "'QA', 'OM', 'KW', 'EG', 'MA', 'DZ', 'TN', 'LB', 'JO', 'PS', 'IN', 'BY', 'KZ', 'MD', 'UA', 'AL', "
                  "'BA', 'HR', 'ME', 'MK', 'RS', 'SI', 'KR', 'BD', 'PK', 'LK', 'GH', 'KE', 'NG', 'TZ', 'UG', 'AG', "
                  "'AM', 'BS', 'BB', 'BZ', 'BT', 'BW', 'BF', 'CV', 'CW', 'DM', 'FJ', 'GM', 'GE', 'GD', 'GW', 'GY', "
                  "'HT', 'JM', 'KI', 'LS', 'LR', 'MW', 'MV', 'ML', 'MH', 'FM', 'NA', 'NR', 'NE', 'PW', 'PG', 'WS', "
                  "'SM', 'ST', 'SN', 'SC', 'SL', 'SB', 'KN', 'LC', 'VC', 'SR', 'TL', 'TO', 'TT', 'TV', 'VU', 'AZ', "
                  "'BN', 'BI', 'KH', 'CM', 'TD', 'KM', 'GQ', 'SZ', 'GA', 'GN', 'KG', 'LA', 'MO', 'MR', 'MN', 'NP', "
                  "'RW', 'TG', 'UZ', 'ZW', 'BJ', 'MG', 'MU', 'MZ', 'AO', 'CI', 'DJ', 'ZM', 'CD', 'CG', 'IQ', 'LY', "
                  "'TJ', 'VE', 'ET', 'XK'], 'disc_number': 1, 'duration_ms': 178933, 'explicit': False, "
                  "'external_ids': {'isrc': 'DEEF22010465'}, 'external_urls': {'spotify': "
                  "'https://open.spotify.com/track/0BRXJHRNGQ3W4v9frnSfhu'}, 'href': "
                  "'https://api.spotify.com/v1/tracks/0BRXJHRNGQ3W4v9frnSfhu', 'id': '0BRXJHRNGQ3W4v9frnSfhu', "
                  "'is_local': False, 'name': 'Ave Maria', 'popularity': 4, 'preview_url': "
                  "'https://p.scdn.co/mp3-preview/0fd4e2b58646e6d11164aa7daff514d36c12966e?cid"
                  "=a7a02e00f9664daaa47b8517d1d8bbcb', 'track_number': 11, 'type': 'track', "
                  "'uri': 'spotify:track:0BRXJHRNGQ3W4v9frnSfhu'}")
        print(recommendations)
        assert my_str in recommendations, f"{my_str} not found in the list {recommendations}"


if __name__ == '__main__':
    unittest.main()

