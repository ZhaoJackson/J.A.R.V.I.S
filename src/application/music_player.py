# # src/application/music_player.py
from typing import List, Dict
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from src.commonconst import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    SPOTIFY_SCOPE,
    SPOTIFY_PLAYLISTS
)

# === Spotify Client Initialization ===
def get_spotify_client() -> Spotify:
    return Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE
    ))


# === Play Track by URI (Renamed for clarity) ===
def play_song_by_uri(uri: str) -> dict:
    sp = get_spotify_client()
    try:
        devices = sp.devices().get("devices", [])
        if not devices:
            return {"status": "error", "message": "No active Spotify devices found."}

        device = next((d for d in devices if d["is_active"]), devices[0])
        sp.start_playback(device_id=device["id"], uris=[uri])

        return {"status": "playing", "device": device["name"]}
    except Exception as e:
        return {"status": "error", "message": f"Playback failed: {e}"}


# === Play Song by Keyword Search ===
def search_and_play_by_keyword(keyword: str) -> dict:
    sp = get_spotify_client()
    try:
        results = sp.search(q=keyword, type="track", limit=10)
        tracks = results.get("tracks", {}).get("items", [])
        if not tracks:
            return {
                "status": "error",
                "message": f"No songs found for keyword '{keyword}'.",
                "device": None,
                "playlist": None
            }

        track = tracks[0]
        uri = track["uri"]
        playback = play_song_by_uri(uri)

        return {
            "status": "success" if playback["status"] == "playing" else "error",
            "message": f"Now playing '{track['name']}' by {track['artists'][0]['name']}'",
            "device": playback.get("device"),
            "playlist": f"Search: {keyword}"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Search/playback failed: {e}",
            "device": None,
            "playlist": None
        }


# === Fetch Tracks from Playlist ID ===
def get_tracks_from_playlist(playlist_id: str) -> List[Dict]:
    sp = get_spotify_client()
    try:
        tracks_data = sp.playlist_tracks(playlist_id)
        items = tracks_data.get("items", [])
        result = []
        for item in items:
            track = item.get("track")
            if track:
                result.append({
                    "uri": track["uri"],
                    "name": track["name"],
                    "artist": track["artists"][0]["name"]
                })
        return result
    except Exception:
        return []