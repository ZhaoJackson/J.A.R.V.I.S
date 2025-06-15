# src/application/music_vs_mood.py

from src.commonconst import (
    SPOTIPY_CLIENT_ID,
    SPOTIPY_CLIENT_SECRET,
    SPOTIPY_REDIRECT_URI,
    SPOTIFY_SCOPE,
    OLLAMA_URL,
    OLLAMA_MODEL,
    MOOD_PLAYLISTS
)
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests

# === Spotify Authorization ===
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE
))

def analyze_mood_from_diary(diary_entry: str) -> str:
    """
    Send diary entry to Ollama model and return a simplified mood tag.
    """
    prompt = (
        "You are a mood analysis assistant. Given the following diary entry, return ONLY one word from:\n"
        "[happy, sad, calm, angry, focused].\n\n"
        f'Diary Entry: "{diary_entry}"\n\nRespond with only the word.'
    )
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        mood = response.json().get("response", "").strip().lower()
        return mood if mood in MOOD_PLAYLISTS else "calm"
    except Exception as e:
        print("⚠️ Mood detection failed:", e)
        return "calm"

def play_music_by_mood(mood: str) -> dict:
    """
    Selects and plays a Spotify playlist based on the mood.
    """
    try:
        profile = sp.current_user()
        if profile.get("product") != "premium":
            return {"error": f"Spotify Premium required. Your plan: {profile.get('product')}"}

        playlist_uri = MOOD_PLAYLISTS.get(mood)
        if not playlist_uri:
            return {"error": f"Unsupported mood '{mood}'."}

        devices = sp.devices().get("devices", [])
        if not devices:
            return {"error": "No active Spotify devices found."}

        device = next((d for d in devices if d["is_active"]), devices[0])
        sp.start_playback(device_id=device["id"], context_uri=playlist_uri)

        return {"status": "playing", "mood": mood, "device": device["name"]}
    except Exception as e:
        return {"error": f"Spotify playback failed: {e}"}