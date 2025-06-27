# src/interaction/music_mood/music_vs_mood.py

import random
from typing import Dict
from sentence_transformers import util
from src.application.mood_analyzer import analyze_mood_profile
from src.application.music_player import (
    get_tracks_from_playlist,
    play_entire_playlist,
    search_and_play_by_keyword
)
from src.application.db_manager import log_music_playback, log_music_feedback
from src.commonconst import SPOTIFY_PLAYLISTS, EMBEDDING_MODEL

# === Get One Song Randomly from Playlist ===
def get_random_song_from_playlist(playlist_id: str) -> Dict:
    tracks = get_tracks_from_playlist(playlist_id)
    return random.choice(tracks) if tracks else {}

# === Match Mood to Closest Playlist Name ===
def smart_match_playlist(mood: str) -> str | None:
    playlist_names = list(SPOTIFY_PLAYLISTS.keys())
    mood_embedding = EMBEDDING_MODEL.encode(mood, convert_to_tensor=True)
    playlist_embeddings = EMBEDDING_MODEL.encode(playlist_names, convert_to_tensor=True)

    scores = util.cos_sim(mood_embedding, playlist_embeddings)[0]
    best_index = scores.argmax().item()
    return playlist_names[best_index]

# === Main Entry Function ===
def play_music_by_emotion_text(text: str, source: str = "fastapi") -> Dict:
    try:
        # Step 1: Analyze mood from emotion
        mood_result = analyze_mood_profile(text)
        mood_description = mood_result.get("mood", "calm")

        # Step 2: Match mood to playlist
        playlist_name = smart_match_playlist(mood_description)
        playlist_id = SPOTIFY_PLAYLISTS.get(playlist_name)

        if playlist_id:
            # Step 3: Play playlist and log
            result = play_entire_playlist(playlist_id)
            if result["status"] != "playing":
                return {
                    "status": "error",
                    "mood": mood_description,
                    "message": result.get("message", "Playback failed."),
                    "device": None,
                    "playlist": playlist_name
                }

            log_music_playback(mood_description, playlist_id, result.get("device", "unknown"))

            return {
                "status": "success",
                "mood": mood_description,
                "message": f"🎶 Shuffling playlist for your mood: '{playlist_name}'",
                "device": result.get("device"),
                "playlist": playlist_name,
                "feedback_prompt": f"🧠 Did this playlist match your emotion '{text}'? (yes/no)"
            }

        # Step 4: Fallback - search by mood
        fallback_result = search_and_play_by_keyword(mood_description)
        return {
            **fallback_result,
            "mood": mood_description,
            "feedback_prompt": f"🎧 Was this fallback song okay for your emotion '{text}'? (yes/no)"
        }

    except Exception as e:
        return {
            "status": "error",
            "mood": "unknown",
            "message": f"Unexpected error: {str(e)}",
            "device": None,
            "playlist": None
        }

# === Feedback Logger ===
def record_music_feedback(
    user_input: str,
    detected_mood: str,
    playlist: str,
    song_name: str,
    user_feedback: str,
    source: str
) -> str:
    try:
        log_music_feedback(
            user_input=user_input,
            detected_mood=detected_mood,
            playlist=playlist,
            song_name=song_name,
            user_feedback=user_feedback,
            source=source
        )
        return "✅ Feedback recorded."
    except Exception as e:
        return f"❌ Failed to log feedback: {str(e)}"