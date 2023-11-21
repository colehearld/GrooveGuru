import ast

from flask import Flask, render_template
from flask_cors import CORS

from engine import get_song_data, init_userdata, sp_login, spotify_data_path

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    song_data = fetch_data()

    result = process_data(song_data)

    return render_template('index.html', songs=result)


def fetch_data():
    return get_song_data(sp_login, init_userdata(), spotify_data_path)


import ast

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



if __name__ == '__main__':
    app.run(debug=True)