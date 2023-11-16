import unittest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np
import engine
import json


class TestSpotifyFunctions(unittest.TestCase):
    @patch('spotipy.Spotify')
    def test_get_recent_tracks(self, mock_spotify):
        # Mock the Spotify instance
        sp_instance = mock_spotify.return_value
        sp_instance.current_user_recently_played.return_value = {'items': [{'track': {'id': '123'}}, {'track': {'id': '456'}}], 'next': None}

        # Call the function to test
        tracks, dates = engine.get_recent_tracks(sp_instance, 2)

        # Perform assertions
        self.assertEqual(tracks, ['123', '456'])
        self.assertTrue(all(isinstance(date, str) for date in dates))

    @patch('spotipy.Spotify')
    def test_get_tracks(self, mock_spotify):
        # Mock the Spotify instance
        sp_instance = mock_spotify.return_value
        sp_instance.track.return_value = {'name': 'Test Track'}

        # Call the function to test
        track_info = engine.get_tracks(sp_instance, '123')

        # Perform assertions
        self.assertEqual(track_info['name'], 'Test Track')

    def test_get_tracks_id(self):
        # Test with sample data
        tracks = [{'track': {'id': '123'}}, {'track': {'id': '456'}}]
        track_ids = engine.get_tracks_id(tracks)

        # Perform assertions
        self.assertEqual(track_ids, ['123', '456'])

    def test_get_date_played(self):
        # Test with sample data
        tracks = [{'played_at': '2022-01-01'}, {'played_at': '2022-01-02'}]
        dates_played = engine.get_date_played(tracks)

        # Perform assertions
        self.assertEqual(dates_played, ['2022-01-01', '2022-01-02'])

    @patch('spotipy.Spotify')
    def test_get_audio_features(self, mock_spotify):
        # Mock the Spotify instance
        sp_instance = mock_spotify.return_value
        sp_instance.audio_features.return_value = [{'acousticness': 0.5, 'danceability': 0.7}]

        # Call the function to test
        audio_features = engine.get_audio_features(sp_instance, ['123'])

        # Perform assertions
        self.assertEqual(audio_features, [{'acousticness': 0.5, 'danceability': 0.7}])


    # TODO: Write test for get_recommendations, imit_userdata, filter_recs


if __name__ == '__main__':
    unittest.main()

