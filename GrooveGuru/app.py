import ast

from flask import Flask, render_template

from engine import get_recommendations, init_userdata
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from credentials import client_id, client_secret, redirect_uri

sp_login = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                              scope='user-read-recently-played'))

app = Flask(__name__)

@app.route('/')
def index():
    song_data = fetch_data()

    # Process the result
    result = process_data(song_data)

    # Render HTML
    return render_template('index.html', songs=result)

def fetch_data():
    return get_recommendations(sp_login, init_userdata())

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

        song_info = {
            'photo': image_url,
            'name': artists_info.get('name', ''),
            'song_name': item.get('song_name', ''),
            'date': album_info.get('release_date', '')
        }

        extracted_data.append(song_info)

    return extracted_data

if __name__ == '__main__':
    app.run(debug=True)