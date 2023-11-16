from flask import Flask, render_template, jsonify
from engine import get_recommendations
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from credentials import client_id, client_secret, redirect_uri

sp_login = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                              scope='user-read-recently-played'))


app = Flask(__name__)

@app.route('/get_recs')
def get_recs():
    recs = get_recommendations(sp_login, "userdata.db")
    return jsonify(recs)


@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)