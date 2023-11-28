import re
import time

import spotipy
from spotipy import SpotifyException
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors

from credentials import client_id, client_secret, redirect_uri
import sqlite3
import logging
from shared_data import liked_songs, disliked_songs

spotify_data_path = 'C:/Users/hearl/Downloads/Spotify 600/tracks.csv'  # CHANGE TO YOUR PATH
userdata_path = "userdata.db"


def get_spotify_auth():
    scope = 'user-read-recently-played'
    sp_oauth = SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri, scope=scope)

    retry_attempts = 3
    current_attempt = 1

    while current_attempt <= retry_attempts:
        try:
            token_info = sp_oauth.get_cached_token()

            if not token_info:
                auth_url = sp_oauth.get_authorize_url()
                print(f"Please visit this URL to authorize the application: {auth_url}")
                response = input("Paste the redirect URL here: ")

                token_info = sp_oauth.get_access_token(response)

            return spotipy.Spotify(auth=token_info['access_token'])

        except SpotifyException as e:
            if e.http_status == 429:  # Rate limiting error
                # Extract the Retry-After header or use a default wait time
                wait_time = int(e.headers.get('Retry-After', 5))
                print(f"Rate limit exceeded. Retrying after {wait_time} seconds.")
                time.sleep(wait_time)
                current_attempt += 1
            else:
                # Log other SpotifyException errors
                logging.error(f"Spotify API error: {e}")
                raise

    # If all retry attempts fail, raise an exception
    raise Exception("Unable to obtain Spotify authentication after multiple attempts.")


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
    audio_features = [{'acousticness': 0.5, 'danceability': 0.5, 'energy': 0.5, 'instrumentalness': 0.5, 'liveness': 0.5,
                        'loudness': 0.5, 'speechiness': 0.5, 'tempo': 0.5, 'valence': 0.5, 'time_signature': 0.5,
                        'key': 0.5, 'mode': 0.5}]
    return audio_features


def load_data(sdp):
    try:
        spotify_data = pd.read_csv(sdp)
        spotify_data = spotify_data.dropna(axis=0)
    except Exception as e:
        logging.critical(f"Error in load_data {str(e)}")
    return spotify_data


def create_tables(cursor):
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tracks (
            id TEXT PRIMARY KEY,
            audio_features TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS liked_songs (
            id TEXT PRIMARY KEY,
            FOREIGN KEY (id) REFERENCES tracks(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS disliked_songs (
            id TEXT PRIMARY KEY,
            FOREIGN KEY (id) REFERENCES tracks(id)
        )
    ''')


def init_userdata(udp):
    try:
        all_tracks, dates_played = get_recent_tracks(get_spotify_auth(), 20)
        song_data_list = []

        conn = sqlite3.connect(udp)
        cursor = conn.cursor()

        create_tables(cursor)

        for track_id in liked_songs:
            cursor.execute('INSERT OR IGNORE INTO liked_songs (id) VALUES (?)', (track_id,))

        for track_id in disliked_songs:
            cursor.execute('INSERT OR IGNORE INTO disliked_songs (id) VALUES (?)', (track_id,))

        for track_id in all_tracks:
            cursor.execute('SELECT * FROM tracks WHERE id = ?', (track_id,))
            existing_track = cursor.fetchone()

            if not existing_track:
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


def update_liked_songs(likes):
    try:
        conn = sqlite3.connect(userdata_path)
        cursor = conn.cursor()

        for song in likes:
            link = song['link']
            song_id = re.search(r'/track/([a-zA-Z0-9]+)$', link).group(1)
            cursor.execute('INSERT OR IGNORE INTO liked_songs (id) VALUES (?)', (song_id,))

        conn.commit()
        conn.close()

    except Exception as e:
        logging.error(f"Error in update_liked_songs: {str(e)}")


def update_disliked_songs(dislikes):
    try:
        conn = sqlite3.connect(userdata_path)
        cursor = conn.cursor()

        for song in dislikes:
            link = song['link']
            song_id = re.search(r'/track/([a-zA-Z0-9]+)$', link).group(1)
            cursor.execute('INSERT OR IGNORE INTO disliked_songs (id) VALUES (?)', (song_id,))

        conn.commit()
        conn.close()

    except Exception as e:
        logging.error(f"Error in update_disliked_songs: {str(e)}")


def get_rec_indices(udp, sdp):
    try:
        conn = sqlite3.connect(udp)
        cursor = conn.cursor()

        # Fetch audio features for tracks that are not disliked and not liked
        cursor.execute('''
            SELECT audio_features 
            FROM tracks 
            WHERE id NOT IN (SELECT id FROM disliked_songs) AND id NOT IN (SELECT id FROM liked_songs)
        ''')
        user_data = cursor.fetchall()

        # Convert fetched data to a list of dictionaries
        user_data = [{'audio_features': json.loads(row[0])} for row in user_data]

        # Load Spotify data
        spotify_data = load_data(sdp)
        spotify_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                             'speechiness', 'tempo', 'valence', 'time_signature', 'key', 'mode']
        X = spotify_data[spotify_features].values

        # Extract audio features from user data
        Y = np.array([[track['audio_features'][feature] for feature in spotify_features] for track in user_data])

        # Consider liked songs in the recommendation algorithm
        cursor.execute('SELECT audio_features FROM tracks WHERE id IN (SELECT id FROM liked_songs)')
        liked_songs_data = cursor.fetchall()

        if liked_songs_data:
            liked_songs_data = [{'audio_features': json.loads(row[0])} for row in liked_songs_data]
            Y = np.concatenate([Y, np.array([[track['audio_features'][feature] for feature in spotify_features] for track in liked_songs_data])])

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

        recommended_songs_id_name = [(spotifydata.iloc[neighbor_index]['id'], spotifydata.iloc[neighbor_index]['name'])
                                      for neighbor_index in indices.flatten()]

        recommendations = []

        conn = sqlite3.connect(udp)
        cursor = conn.cursor()

        for id, name in recommended_songs_id_name:
            # Check if the recommendation is liked or disliked
            cursor.execute('SELECT id FROM liked_songs WHERE id = ?', (str(id),))
            liked_song = cursor.fetchone()

            cursor.execute('SELECT id FROM disliked_songs WHERE id = ?', (str(id),))
            disliked_song = cursor.fetchone()

            if liked_song or disliked_song:
                print(f"The recommendation '{name}' with ID {id} is already liked or disliked. Choosing another recommendation.")
                continue

            rec_song_data = get_tracks(sp, str(id))
            rec_song_data['song_name'] = name
            rec_song_data_str = rec_song_data.__str__()
            recommendations.append(rec_song_data_str)

        conn.close()

    except Exception as e:
        logging.error(f"Error in get_song_data {str(e)}")

    return recommendations


if __name__ == "__main__":
    print(get_song_data(get_spotify_auth(), userdata_path, spotify_data_path))