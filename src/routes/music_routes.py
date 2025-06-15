# src/routes/music_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
from src.application.mood_analyzer import analyze_mood_from_text
from src.application.music_player import play_music_by_mood

router = APIRouter()

class MoodInput(BaseModel):
    text: str

class MusicResponse(BaseModel):
    status: str
    mood: str
    device: Optional[str] = None
    message: str

@router.post("/music", response_model=MusicResponse)
async def music_by_mood(request: MoodInput):
    """
    Accepts free-form text input, detects mood via LLM,
    and plays a Spotify playlist matched to the mood.

    Example input:
    {
        "text": "I'm feeling anxious but want to calm down"
    }
    """
    user_input = request.text

    if not user_input:
        return {
            "status": "error",
            "mood": "unknown",
            "device": None,
            "message": "Missing input text"
        }

    # Step 1: Analyze Mood via Ollama
    mood = analyze_mood_from_text(user_input)

    # Step 2: Trigger Spotify Playback
    result = play_music_by_mood(mood)

    # Step 3: Compose API Response
    if result.get("status") == "playing":
        return {
            "status": "success",
            "mood": mood,
            "device": result.get("device"),
            "message": f"🎵 Now playing a {mood} playlist on {result.get('device')}"
        }
    else:
        return {
            "status": "error",
            "mood": mood,
            "device": None,
            "message": result.get("error", "Playback failed")
        }