# src/application/music_player.py

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from src.commonconst import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    SPOTIFY_SCOPE
)

def get_spotify_client() -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE
    ))

def play_song_by_name(song_name: str) -> dict:
    """
    Searches for a track by name and plays it on the user's active device.
    """
    sp = get_spotify_client()

    try:
        results = sp.search(q=song_name, type="track", limit=1)
        tracks = results.get("tracks", {}).get("items", [])

        if not tracks:
            return {"status": "error", "message": "Song not found."}

        track = tracks[0]
        uri = track["uri"]

        devices = sp.devices().get("devices", [])
        if not devices:
            return {"status": "error", "message": "No active Spotify devices found."}

        device = next((d for d in devices if d["is_active"]), devices[0])
        sp.start_playback(device_id=device["id"], uris=[uri])

        return {
            "status": "playing",
            "track": track["name"],
            "artist": track["artists"][0]["name"],
            "device": device["name"]
        }
    except Exception as e:
        return {"status": "error", "message": f"Playback failed: {e}"}