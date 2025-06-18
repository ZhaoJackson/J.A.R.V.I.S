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
from src.application.db_manager import log_music_playback
from src.commonconst import SPOTIFY_PLAYLISTS, EMBEDDING_MODEL

def get_random_song_from_playlist(playlist_id: str) -> Dict:
    tracks = get_tracks_from_playlist(playlist_id)
    return random.choice(tracks) if tracks else {}

def smart_match_playlist(mood: str) -> str | None:
    """
    Use embedding similarity to match mood to closest playlist name (key).
    """
    playlist_names = list(SPOTIFY_PLAYLISTS.keys())
    mood_embedding = EMBEDDING_MODEL.encode(mood, convert_to_tensor=True)
    playlist_embeddings = EMBEDDING_MODEL.encode(playlist_names, convert_to_tensor=True)

    scores = util.cos_sim(mood_embedding, playlist_embeddings)[0]
    best_index = scores.argmax().item()
    return playlist_names[best_index]  # return playlist name (not ID)

def play_music_by_emotion_text(text: str) -> Dict:
    try:
        # Step 1: Analyze mood from user input
        mood_result = analyze_mood_profile(text)
        mood_description = mood_result.get("mood", "calm")

        # Step 2: Match mood to best playlist name
        playlist_name = smart_match_playlist(mood_description)
        playlist_id = SPOTIFY_PLAYLISTS.get(playlist_name)

        if playlist_id:
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
                "playlist": playlist_name
            }

        # Step 3: Fallback – search and play based on mood keyword
        fallback_result = search_and_play_by_keyword(mood_description)
        return {
            **fallback_result,
            "mood": mood_description
        }

    except Exception as e:
        return {
            "status": "error",
            "mood": "unknown",
            "message": f"Unexpected error: {str(e)}",
            "device": None,
            "playlist": None
        }