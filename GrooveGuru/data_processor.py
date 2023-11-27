import ast

from engine import get_song_data, get_spotify_auth, spotify_data_path, userdata_path

var = (), spotify_data_path, userdata_path


def fetch_and_process_data():
    song_data = fetch_data()
    return process_data(song_data)


def fetch_data():
    return get_song_data(get_spotify_auth(), userdata_path, spotify_data_path)


def process_data(data_list):
    extracted_data = []

    for item in data_list:
        try:
            item_dict = ast.literal_eval(item)
        except (ValueError, SyntaxError):
            continue

        album_info = item_dict.get('album', {})
        artists_info = item_dict.get('artists', [{}])[0]
        images = album_info.get('images', [])
        image_url = images[0]['url'] if images else None

        external_urls = item_dict.get('external_urls', {})

        song_info = {
            'photo': image_url,
            'name': artists_info.get('name', ''),
            'song_name': item_dict.get('song_name', ''),
            'date': album_info.get('release_date', ''),
            'song_link': external_urls.get('spotify', '')
        }

        extracted_data.append(song_info)

    return extracted_data
