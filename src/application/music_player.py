# src/application/music_player.py

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

# === Play One Song by URI ===
def play_song_by_uri(uri: str) -> dict:
    if not is_spotify_configured():
        return simulate_music_playback("unknown", "Spotify Track")
    
    sp = get_spotify_client()
    try:
        devices = sp.devices().get("devices", [])
        if not devices:
            return {"status": "error", "message": "No active Spotify devices found."}

        device = next((d for d in devices if d["is_active"]), devices[0])
        sp.start_playback(device_id=device["id"], uris=[uri])

        return {"status": "playing", "device": device["name"]}
    except Exception as e:
        error_str = str(e).lower()
        # Check for authentication/client errors - fall back to simulation
        if any(error_type in error_str for error_type in ['invalid_client', 'unauthorized', 'authentication', 'token']):
            print(f"🎵 Spotify authentication error, falling back to simulation mode: {e}")
            return simulate_music_playback("unknown", "Spotify Track")
        else:
            return {"status": "error", "message": f"Playback failed: {e}"}

# === Play Playlist ===
def play_playlist(playlist_id: str) -> dict:
    """Play a playlist on Spotify"""
    playlist_name = next((name.title() for name, id_val in SPOTIFY_PLAYLISTS.items() if id_val == playlist_id), "Unknown")
    
    if not is_spotify_configured():
        return {
            "status": "error", 
            "message": "❌ Spotify not configured. Please set SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET in your .env file"
        }
    
    try:
        sp = get_spotify_client()
        devices = sp.devices().get("devices", [])
        
        if not devices:
            return {
                "status": "error",
                "message": "❌ No Spotify devices found. Please open Spotify on your phone/computer first"
            }
        
        # Use active device or first available device
        device = next((d for d in devices if d["is_active"]), devices[0])
        
        # Start playlist playback with shuffle
        sp.shuffle(state=True, device_id=device["id"])
        sp.start_playback(device_id=device["id"], context_uri=f"spotify:playlist:{playlist_id}")
        
        return {
            "status": "success", 
            "device": device["name"], 
            "playlist": playlist_name,
            "message": f"🎵 Playing {playlist_name} playlist on {device['name']}"
        }
        
    except Exception as e:
        error_msg = str(e)
        if "invalid_client" in error_msg.lower():
            return {
                "status": "error",
                "message": "❌ Invalid Spotify credentials. Please check your SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET"
            }
        elif "unauthorized" in error_msg.lower():
            return {
                "status": "error", 
                "message": "❌ Spotify authorization failed. Please re-authorize the app"
            }
        else:
            return {
                "status": "error",
                "message": f"❌ Spotify error: {error_msg}"
            }

# === Search and Play by Keyword ===
def search_and_play_by_keyword(keyword: str) -> dict:
    if not is_spotify_configured():
        return simulate_music_playback(keyword)
    
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
        error_str = str(e).lower()
        # Check for authentication/client errors - fall back to simulation
        if any(error_type in error_str for error_type in ['invalid_client', 'unauthorized', 'authentication', 'token']):
            print(f"🎵 Spotify authentication error, falling back to simulation mode: {e}")
            return simulate_music_playback(keyword)
        else:
            return {
                "status": "error",
                "message": f"Search/playback failed: {e}",
                "device": None,
                "playlist": None
            }

# === Fetch Tracks from Playlist ID ===
def get_tracks_from_playlist(playlist_id: str) -> List[Dict]:
    if not is_spotify_configured():
        # Return sample tracks for simulation
        return [
            {"uri": "spotify:track:sample1", "name": "Sample Song 1", "artist": "Demo Artist 1"},
            {"uri": "spotify:track:sample2", "name": "Sample Song 2", "artist": "Demo Artist 2"},
            {"uri": "spotify:track:sample3", "name": "Sample Song 3", "artist": "Demo Artist 3"}
        ]
    
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

# === Check if Spotify is configured ===
def is_spotify_configured() -> bool:
    """Check if Spotify credentials are properly set"""
    return bool(SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET and 
                SPOTIPY_CLIENT_ID != "your_spotify_client_id" and 
                SPOTIPY_CLIENT_SECRET != "your_spotify_client_secret")

# === Simulation Mode Functions ===
def simulate_music_playback(mood: str, playlist_name: str = None) -> Dict:
    """Simulate music playback when Spotify is not configured"""
    import random
    
    # Simulate realistic responses
    devices = ["iPhone", "MacBook Pro", "iPad", "Smart Speaker", "Headphones"]
    device = random.choice(devices)
    
    return {
        "status": "success", 
        "device": f"Jackson's {device}",
        "mode": "simulation",
        "playlist": playlist_name or "Unknown",
        "message": f"🎵 [DEMO] Music simulation active - Spotify not configured"
    }

# === Configuration Status Function ===
def get_music_system_status() -> Dict:
    """Get the current status of the music system"""
    spotify_configured = is_spotify_configured()
    
    return {
        "spotify_configured": spotify_configured,
        "mode": "production" if spotify_configured else "simulation",
        "playlists_configured": len([p for p in SPOTIFY_PLAYLISTS.values() if p]) if spotify_configured else 6,
        "message": "Spotify integration active" if spotify_configured else "Running in demo mode - configure Spotify for real playback"
    }