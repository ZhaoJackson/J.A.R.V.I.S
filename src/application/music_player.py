# src/application/music_player.py

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from src.commonconst import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    SPOTIFY_SCOPE,
    MOOD_PLAYLISTS
)

def get_spotify_client() -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE
    ))

def play_music_by_mood(mood: str) -> dict:
    sp = get_spotify_client()
    playlist_uri = MOOD_PLAYLISTS.get(mood.lower())

    if not playlist_uri:
        return {"status": "error", "message": f"Unrecognized mood: {mood}"}

    try:
        devices = sp.devices()
        if not devices["devices"]:
            return {"status": "error", "message": "No active Spotify devices found."}

        device_id = devices["devices"][0]["id"]
        device_name = devices["devices"][0]["name"]

        sp.start_playback(device_id=device_id, context_uri=playlist_uri)

        return {
            "status": "playing",
            "mood": mood,
            "playlist": playlist_uri,
            "device": device_name
        }

    except Exception as e:
        return {"status": "error", "message": str(e)}