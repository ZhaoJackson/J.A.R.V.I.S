# src/application/music_engine.py - Music Selection and Playback

from typing import Dict
from sentence_transformers import util
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from src.commonconst import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET, 
    SPOTIPY_REDIRECT_URI,
    SPOTIFY_SCOPE,
    SPOTIFY_PLAYLISTS,
    EMBEDDING_MODEL
)
from src.modeling.intelligent_selector import intelligent_selector

def get_spotify_client() -> Spotify:
    """Initialize Spotify client"""
    return Spotify(auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URI,
        scope=SPOTIFY_SCOPE
    ))

def is_spotify_configured() -> bool:
    """Check if Spotify credentials are properly set"""
    return bool(SPOTIPY_CLIENT_ID and SPOTIPY_CLIENT_SECRET and 
                SPOTIPY_CLIENT_ID != "your_spotify_client_id" and 
                SPOTIPY_CLIENT_SECRET != "your_spotify_client_secret")

def match_emotion_to_playlist(emotion: str, emotional_context: str = "") -> Dict:
    """Use ML model to intelligently select playlist"""
    return intelligent_selector.select_optimal_playlist(emotion, emotional_context)

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

def play_music_for_emotion(text: str, emotion: str) -> dict:
    """Main function: match emotion to music and play"""
    # Use intelligent selector for playlist
    selection_result = match_emotion_to_playlist(emotion, text)
    playlist_name = selection_result["playlist"]
    playlist_confidence = selection_result["confidence"]
    playlist_id = SPOTIFY_PLAYLISTS.get(playlist_name)
    
    if not playlist_id:
        return {"status": "error", "message": "❌ No playlist found for this emotion"}
    
    # Try to play the playlist
    result = play_playlist(playlist_id)
    
    if result.get("status") == "success":
        # Real Spotify playback successful
        music_message = f"🎶 AI selected this music to support your {emotion} emotional state (confidence: {playlist_confidence:.2f})"
        return {
            "status": "success",
            "emotion": emotion,
            "playlist": playlist_name,
            "device": result.get("device"),
            "confidence": playlist_confidence,
            "message": f"🎵 {playlist_name.title()} playlist now playing on {result.get('device')}\n{music_message}"
        }
    else:
        # Spotify error - return the error message
        return {
            "status": "error",
            "emotion": emotion,
            "playlist": playlist_name,
            "device": None,
            "message": result.get("message", "❌ Music playbook failed")
        }
