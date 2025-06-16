# src/application/music_vs_mood.py

from src.application.mood_analyzer import analyze_mood
from src.application.music_player import get_spotify_client
from src.application.db_manager import log_mood_analysis, log_music_playback
from src.commonconst import MOOD_PLAYLISTS

def play_music_by_emotional_text(text: str) -> dict:
    """
    Given emotional diary input, infer mood, log analysis, and play music.
    """
    # Step 1: Detect mood from text
    mood = analyze_mood(text)

    # Step 2: Log mood analysis
    log_mood_analysis(text, mood)

    # Step 3: Look up playlist
    playlist_uri = MOOD_PLAYLISTS.get(mood)
    if not playlist_uri:
        return {
            "status": "error",
            "mood": mood,
            "message": f"No playlist found for detected mood: '{mood}'"
        }

    # Step 4: Play playlist via Spotify
    try:
        sp = get_spotify_client()
        devices = sp.devices().get("devices", [])
        if not devices:
            return {
                "status": "error",
                "mood": mood,
                "message": "No active Spotify devices found."
            }

        device = next((d for d in devices if d["is_active"]), devices[0])
        sp.start_playback(device_id=device["id"], context_uri=playlist_uri)

        # Step 5: Log music playback
        log_music_playback(mood, playlist_uri, device["name"])

        return {
            "status": "playing",
            "mood": mood,
            "playlist": playlist_uri,
            "device": device["name"],
            "message": f"🎵 Now playing a '{mood}' playlist on {device['name']}"
        }

    except Exception as e:
        return {
            "status": "error",
            "mood": mood,
            "message": f"Playback failed: {e}"
        }