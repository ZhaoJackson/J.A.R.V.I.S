import random
from typing import Dict

from src.application.mood_analyzer import analyze_mood_profile
from src.application.music_player import (
    get_tracks_from_playlist,
    play_song_by_uri,
    search_and_play_by_keyword
)
from src.application.db_manager import log_music_playback
from src.commonconst import SPOTIFY_PLAYLISTS


def get_random_song_from_playlist(playlist_id: str) -> Dict:
    tracks = get_tracks_from_playlist(playlist_id)
    if not tracks:
        return {}

    track = random.choice(tracks)
    return {
        "name": track["name"],
        "artist": track["artist"],
        "uri": track["uri"]
    }


# def match_playlist_for_mood(mood: str) -> str | None:
#     return SPOTIFY_PLAYLISTS.get(mood.strip().lower())

def match_playlist_for_mood(mood: str) -> str | None:
    mood_clean = mood.strip().lower()
    for key in SPOTIFY_PLAYLISTS:
        if key.lower() == mood_clean:
            return SPOTIFY_PLAYLISTS[key]
    return None

def play_music_by_emotion_text(text: str) -> Dict:
    try:
        # Step 1: Get mood label from LLM
        mood_result = analyze_mood_profile(text)
        mood = mood_result.get("mood", "Calm")

        # Step 2: Match playlist
        playlist_id = match_playlist_for_mood(mood)

        if playlist_id:
            song = get_random_song_from_playlist(playlist_id)
            if not song:
                return {
                    "status": "error",
                    "mood": mood,
                    "message": f"No songs available in playlist for '{mood}'.",
                    "device": None,
                    "playlist": mood
                }

            result = play_song_by_uri(song["uri"])
            if result["status"] != "playing":
                return {
                    "status": "error",
                    "mood": mood,
                    "message": result.get("message", "Playback failed."),
                    "device": None,
                    "playlist": mood
                }

            log_music_playback(mood, song["uri"], result.get("device", "unknown"))

            return {
                "status": "success",
                "mood": mood,
                "message": f"Now playing '{song['name']}' by {song['artist']}",
                "device": result.get("device"),
                "playlist": mood
            }

        # Step 3: Fallback search
        fallback_result = search_and_play_by_keyword(mood)
        return {
            **fallback_result,
            "mood": mood
        }

    except Exception as e:
        return {
            "status": "error",
            "mood": "unknown",
            "message": f"Unexpected error: {str(e)}",
            "device": None,
            "playlist": None
        }