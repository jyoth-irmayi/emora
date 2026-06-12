# moods/audius_service.py

import requests

MOOD_QUERIES = {
    'happy': 'happy',
    'sad': 'sad',
    'healing': 'healing',
    'motivated': 'motivation',
    'calm': 'relaxing',
}

def get_songs(mood):

    query = MOOD_QUERIES.get(mood, 'music')

    host_response = requests.get(
        "https://api.audius.co"
    )

    host = host_response.json()['data'][0]

    response = requests.get(
        f"{host}/v1/tracks/search",
        params={
            'query': query,
            'limit': 10
        }
    )

    data = response.json()
    songs = []

    if 'data' in data:

        for track in data['data']:

            songs.append({
                'title': track['title'],
                'artist': track['user']['name'],
                'image': track.get('artwork', {}).get('480x480'),
                'track_id': track['id'],
                'stream_url': f"{host}/v1/tracks/{track['id']}/stream"
            })

    return songs