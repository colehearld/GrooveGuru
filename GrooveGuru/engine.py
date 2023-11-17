import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from credentials import client_id, client_secret, redirect_uri
import sqlite3

sp_login = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                              scope='user-read-recently-played'))

spotify_data_path = 'C:/Users/hearl/Downloads/Spotify 600/tracks.csv'  # CHANGE TO YOUR PATH
userdata_path = "userdata.db"


def get_recent_tracks(sp, n_tracks):
    results = sp.current_user_recently_played()

    tracks = get_tracks_id(results['items'])
    dates = get_date_played(results['items'])

    while results['next'] and len(tracks) < n_tracks:
        results = sp.next(results)
        tracks.extend(get_tracks_id(results['items']))
        dates.extend(get_date_played(results['items']))

    return tracks, dates


def get_tracks(sp, track_id):
    track = sp.track(track_id)
    return track


def get_tracks_id(tracks):
    track_ids = [item['track']['id'] for item in tracks if item['track'] and 'id' in item['track']]
    return track_ids


def get_date_played(tracks):
    dates_played = [item['played_at'] for item in tracks if 'played_at' in item]
    return dates_played


def get_audio_features(sp, track_ids):
    audio_features = sp.audio_features(tracks=track_ids)
    return audio_features


def get_recommendations(sp, user_data_path, spotify_data_path):
    spotify_data = pd.read_csv(spotify_data_path)

    spotify_data = spotify_data.dropna(axis=0)

    spotify_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                        'speechiness', 'tempo', 'valence', 'time_signature', 'key', 'mode']
    X = spotify_data[spotify_features].values

    # Connect to the SQLite database
    conn = sqlite3.connect(user_data_path)
    cursor = conn.cursor()

    # Read user data from the 'tracks' table in the SQLite database
    cursor.execute('SELECT audio_features FROM tracks')
    user_data = cursor.fetchall()

    # Convert the fetched data to a list of dictionaries
    user_data = [{'audio_features': json.loads(row[0])} for row in user_data]

    # Extract audio features from user data
    Y = np.array([[track['audio_features'][feature] for feature in spotify_features] for track in user_data])

    # Calculate the mean of the user's listening history
    mean_features = np.mean(Y, axis=0, keepdims=True)

    # Initialize the NearestNeighbors model for the dataset 'X'
    nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X)

    # Find the nearest neighbor in X for the mean features
    distances, indices = nbrs.kneighbors(mean_features)

    # Print the names of the closest indices
    recommended_songs_id_name = [(spotify_data.iloc[neighbor_index]['id'], spotify_data.iloc[neighbor_index]['name'])
                                 for neighbor_index in indices.flatten()]

    recommendations = []
    for id, _ in recommended_songs_id_name:
        rec_song_data = get_tracks(sp, str(id))
        rec_song_data_str = rec_song_data.__str__()
        # filtered = filter_recommendation(rec_song_data_str)
        recommendations.append(rec_song_data_str)

    conn.close()

    return recommendations


def init_userdata(userdata_path):
    all_tracks, dates_played = get_recent_tracks(sp_login, 20)
    song_data_list = []

    conn = sqlite3.connect(userdata_path)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id TEXT PRIMARY KEY,
            audio_features TEXT
        )
    ''')

    for track_id in all_tracks:
        audio_features = get_audio_features(sp_login, [track_id])[0]

        cursor.execute('''
            INSERT OR IGNORE INTO tracks (id, audio_features)
            VALUES (?, ?)
        ''', (track_id, json.dumps(audio_features)))

        song_data = {
            "id": track_id,
            "audio_features": audio_features
        }

        song_data_list.append(song_data)

    conn.commit()
    conn.close()

    return userdata_path


if __name__ == "__main__":
    print(get_recommendations(sp_login, init_userdata()))
