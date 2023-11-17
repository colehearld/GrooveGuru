import unittest
from unittest.mock import patch
from app import app, fetch_data, process_data

class TestFlaskApp(unittest.TestCase):

    @patch('app.fetch_data', return_value=["{'song_name': 'Song 1', 'artists': [{'name': 'Artist 1'}], 'album': {'images': [{'url': 'image_url_1'}], 'release_date': '2022-01-01'}}"])
    def test_index_route(self, mock_fetch_data):
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)

    @patch('app.ast.literal_eval', return_value={'song_name': 'Song 1', 'artists': [{'name': 'Artist 1'}],
                                                            'album': {'images': [{'url': 'image_url_1'}],
                                                                      'release_date': '2022-01-01'}})
    def test_process_data(self, mock_literal_eval):
        # Mock input data
        data_list = [
            "{'song_name': 'Song 1', 'artists': [{'name': 'Artist 1'}], 'album': {'images': [{'url': 'image_url_1'}], 'release_date': '2022-01-01'}}"]

        # Call the actual function
        result = process_data(data_list)

        # Assert the processed data
        expected_result = [
            {'photo': 'image_url_1', 'name': 'Artist 1', 'song_name': 'Song 1', 'date': '2022-01-01'}
        ]
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
