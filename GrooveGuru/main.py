import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import pandas as pd
import numpy as np
from sklearn.neighbors import NearestNeighbors
from credentials import client_id, client_secret, redirect_uri

sp_login = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri,
                              scope='user-read-recently-played'))


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


def get_recommendations(user_data_path):
    spotify_data_filepath = 'C:/Users/hearl/Downloads/Spotify 600/tracks.csv' # CHANGE TO YOUR PATH
    spotify_data = pd.read_csv(spotify_data_filepath)

    spotify_data = spotify_data.dropna(axis=0)

    spotify_features = ['acousticness', 'danceability', 'energy', 'instrumentalness', 'liveness', 'loudness',
                        'speechiness', 'tempo', 'valence', 'time_signature', 'key', 'mode']
    X = spotify_data[spotify_features].values

    # Load user data from JSON file
    with open(user_data_path) as f:
        user_data = json.load(f)

    # Extract audio features from user data
    user_features = [track['audio_features'] for track in user_data]
    Y = np.array([[track[feature] for feature in spotify_features] for track in user_features])

    # Calculate the mean of the user's listening history
    mean_features = np.mean(Y, axis=0, keepdims=True)

    # Initialize the NearestNeighbors model for the dataset 'X'
    nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X)

    # Find the nearest neighbor in X for the mean features
    distances, indices = nbrs.kneighbors(mean_features)

    # Print the names of the closest indices
    recommended_songs = [spotify_data.iloc[neighbor_index]['id'] for neighbor_index in indices.flatten()]

    return recommended_songs



if __name__ == "__main__":
    all_tracks, dates_played = get_recent_tracks(sp_login, 20)

    song_data_list = []

    for track_id in all_tracks:
        audio_features = get_audio_features(sp_login, [track_id])[0]

        song_data = {
            "id": track_id,
            "audio_features": audio_features
        }

        song_data_list.append(song_data)

    userdata_path = "userdata.json"

    # Convert the list of JSON objects to a JSON file
    with open(userdata_path, "w") as json_file:
        json.dump(song_data_list, json_file, indent=2)

    userdata = pd.read_json(userdata_path)

    recommended_songs = get_recommendations(userdata_path)

    for song_id in recommended_songs:
        song_data = print(get_tracks(sp_login, song_id.__str__()))

