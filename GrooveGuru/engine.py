import re
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

from GrooveGuru import shared_data
from credentials import client_id, client_secret, redirect_uri
import sqlite3
import logging
from shared_data import liked_songs, disliked_songs

sp_login = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                              scope='user-read-recently-played'))

spotify_data_path = 'C:/Users/hearl/Downloads/Spotify 600/tracks.csv'  # CHANGE TO YOUR PATH
userdata_path = "userdata.db"


def get_spotify_auth():
    scope = 'user-read-recently-played'
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope='user-read-recently-played')
    token_info = sp_oauth.get_cached_token()

    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print(f"Please visit this URL to authorize the application: {auth_url}")
        response = input("Paste the redirect URL here: ")

        token_info = sp_oauth.get_access_token(response)
    return spotipy.Spotify(auth=token_info['access_token'])


def get_recent_tracks(sp, n_tracks):
    try:
        results = sp.current_user_recently_played()

        tracks = get_tracks_id(results['items'])
        dates = get_date_played(results['items'])

        while results['next'] and len(tracks) < n_tracks:
            results = sp.next(results)
            tracks.extend(get_tracks_id(results['items']))
            dates.extend(get_date_played(results['items']))
    except Exception as e:
        logging.error(f"Error in get_recent_tracks: {str(e)}")
        raise

    return tracks, dates


def get_tracks(sp, track_id):
    try:
        track = sp.track(track_id)
    except Exception as e:
        logging.error(f"Error in get_tracks: {str(e)}")
    return track


def get_tracks_id(tracks):
    try:
        track_ids = [item['track']['id'] for item in tracks if item['track'] and 'id' in item['track']]
    except Exception as e:
        logging.error(f"Error in get_track_id: {str(e)}")
    return track_ids


def get_date_played(tracks):
    try:
        dates_played = [item['played_at'] for item in tracks if 'played_at' in item]
    except Exception as e:
        logging.error(f"Error in get_date_played: {str(e)}")
    return dates_played


def get_audio_features(sp, track_ids):
    try:
        audio_features = sp.audio_features(tracks=track_ids)
    except Exception as e:
        logging.error(f"Error in get_audio_features {str(e)}")
    return audio_features


def load_data(sdp):
    try:
        spotify_data = pd.read_csv(sdp)
        spotify_data = spotify_data.dropna(axis=0)
    except Exception as e:
        logging.critical(f"Error in load_data {str(e)}")
    return spotify_data


def get_rec_indices(udp, sdp):
    try:
        # Load Spotify data
        spotify_data = load_data(sdp)

        '''
        for song in get_preference(shared_data.disliked_songs):
            if song in spotify_data:
                spotify_data = spotify_data[spotify_data['id'] != song]
                dont recommend song
        '''

        spotify_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                            'speechiness', 'tempo', 'valence', 'time_signature', 'key', 'mode']
        X = spotify_data[spotify_features].values

        # Connect to the SQLite database
        conn = sqlite3.connect(udp)
        cursor = conn.cursor()

        # Read user data from the 'tracks' table in the SQLite database
        cursor.execute('SELECT audio_features FROM tracks')
        user_data = cursor.fetchall()

        # Convert the fetched data to a list of dictionaries
        user_data = [{'audio_features': json.loads(row[0])} for row in user_data]

        # Extract audio features from user data
        Y = np.array([[track['audio_features'][feature] for feature in spotify_features] for track in user_data])

        mean_features = np.mean(Y, axis=0, keepdims=True)

        # Initialize the NearestNeighbors model for the dataset 'X'
        nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X)

        # Find the nearest neighbor in X for the mean features
        distances, indices = nbrs.kneighbors(mean_features)

        conn.close()

    except sqlite3.Error as sqlite_error:
        logging.error(f"SQLite error in get_rec_indices: {sqlite_error}")
        raise
    except Exception as e:
        logging.error(f"Error in get_rec_indices: {str(e)}")
        raise
    return indices, spotify_data


def get_song_data(sp, udp, sdp):
    try:
        udp = init_userdata(udp)
        indices, spotifydata = get_rec_indices(udp, sdp)

        # get the names and ids of the closest indices
        recommended_songs_id_name = [(spotifydata.iloc[neighbor_index]['id'], spotifydata.iloc[neighbor_index]['name'])
                                    for neighbor_index in indices.flatten()]

        recommendations = []
        for id, name in recommended_songs_id_name:
            rec_song_data = get_tracks(sp, str(id))
            rec_song_data['song_name'] = name  # adds songs name to data
            rec_song_data_str = rec_song_data.__str__()
            recommendations.append(rec_song_data_str)
    except Exception as e:
        logging.error(f"Error in get_song_data {str(e)}")
    return recommendations


def init_userdata(udp):
    try:
        all_tracks, dates_played = get_recent_tracks(get_spotify_auth(), 20)
        song_data_list = []

        conn = sqlite3.connect(udp)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tracks (
                id TEXT PRIMARY KEY,
                audio_features TEXT
            )
        ''')

        for track_id in all_tracks:
            audio_features = get_audio_features(get_spotify_auth(), [track_id])[0]

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
    
    except sqlite3.Error as sqlite_error:
        logging.error(f"SQLite error in init_userdata: {sqlite_error}")
        raise
    except Exception as e:
        logging.error(f"Error in init_userdata: {str(e)}")
        raise


# This function should be used to get likes or dislikes
# If you would like to retrieve liked songs, use get_preferences(liked_songs) and vice versa
def get_preference(preference_list):
    pattern = r'/track/([a-zA-Z0-9]+)$'

    preferences = []
    for song in preference_list:
        link = song['link']
        song_id = re.search(pattern, link)
        preferences.append(song_id)

    return preferences


if __name__ == "__main__":
    print(get_song_data(get_spotify_auth(), userdata_path, spotify_data_path))

