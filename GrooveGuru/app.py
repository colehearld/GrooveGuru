import ast

from flask import Flask, render_template
from flask_cors import CORS
from engine import get_recommendations, init_userdata, sp_login, spotify_data_path

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    song_data = fetch_data()

    result = process_data(song_data)

    return render_template('index.html', songs=result)


def fetch_data():
    return get_recommendations(sp_login, init_userdata(), spotify_data_path)


def process_data(data_list):
    # Parse the strings into dictionaries
    parsed_data = [ast.literal_eval(item.replace(' song_name:', ',')) for item in data_list]

    # Extract relevant information
    extracted_data = []

    for item in parsed_data:
        album_info = item.get('album', {})
        artists_info = item.get('artists', [{}])[0]
        images = album_info.get('images', [])
        image_url = images[0]['url'] if images else None

        external_urls = item.get('external_urls', {})

        song_info = {
            'photo': image_url,
            'name': artists_info.get('name', ''),
            'song_name': item.get('song_name', ''),
            'date': album_info.get('release_date', ''),
            'song_link': external_urls.get('spotify', '')
        }

        extracted_data.append(song_info)

    return extracted_data


if __name__ == '__main__':
    app.run(debug=True)