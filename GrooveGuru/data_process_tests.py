import unittest
from unittest.mock import patch
from main import app
from data_processor import process_data
import ast

class TestFlaskApp(unittest.TestCase):

    @patch('data_processor.fetch_data', return_value=[
        {'song_link': [{'song_info': 'song_link'}], "song_name": "Song 1", "artists": [{"name": "Artist 1"}],
         "album": {"images": [{"url": "image_url_1"}], "release_date": "2022-01-01"}}])
    def test_index_route(self, mock_fetch_data):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    @patch('ast.literal_eval',
           return_value={'song_link': [{'song_info': 'song_link'}], 'song_name': 'Song 1',
                         'artists': [{'name': 'Artist 1'}],
                         'album': {'images': [{'url': 'image_url_1'}], 'release_date': '2022-01-01'}})
    def test_process_data(self, mock_literal_eval):
        # Mock input data
        data_list = [
            "{'song_link': 'song_link', 'photo': 'image_url_1', 'name': 'Artist 1', 'song_name': 'Song 1', "
            "'date': '2022-01-01'}"
        ]

        result = process_data(data_list)

        # Assert the processed data
        expected_result = [
            {'song_link': '', 'photo': 'image_url_1', 'name': 'Artist 1', 'song_name': 'Song 1', 'date': '2022-01-01'}
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()

