from flask import Flask, jsonify, request
from flask_cors import CORS

from GrooveGuru import shared_data
from data_processor import fetch_data, process_data
from engine import update_liked_songs, update_disliked_songs, get_song_data, get_spotify_auth, userdata_path, \
    spotify_data_path

app = Flask(__name__)
CORS(app)


@app.route('/')
def index():
    try:
        song_data = fetch_data()
        result = process_data(song_data)
        return jsonify({'message': 'Hello from Flask!', 'song': result[0]})
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500


# API endpoint to get all songs
@app.route('/api/songs', methods=['GET'])
def get_all_songs():
    song_data = fetch_data()
    result = process_data(song_data)
    return jsonify(result)


# API endpoint to get a specific song by ID or name
@app.route('/api/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    song_data = fetch_data()
    result = process_data(song_data)

    # Find the specific song
    for song in result:
        if song['song_name'] == song_id or str(song['id']) == song_id:
            return jsonify(song)

    # Return a 404 response if the song is not found
    return jsonify({'error': 'Song not found'}), 404


# API endpoint to update likes and dislikes
@app.route('/api/updateLikesDislikes', methods=['POST'])
def update_likes_dislikes():

    try:
        data = request.json
        likes = shared_data.liked_songs = data.get('likedSongs', [])
        dislikes = shared_data.disliked_songs = data.get('dislikedSongs', [])
        response = {'status': 'success', 'message': 'Likes and dislikes updated successfully.'}
        print('Received liked songs:', likes)
        print('Received disliked songs:', dislikes)

        update_liked_songs(likes)
        update_disliked_songs(dislikes)

    except Exception as e:
        response = {'status': 'error', 'message': str(e)}


    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
