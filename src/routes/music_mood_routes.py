# src/routes/music_mood_routes.py

from fastapi import APIRouter
from pydantic import BaseModel, Field
from src.interaction.music_mood.music_vs_mood import play_music_by_emotion_text

router = APIRouter()


# === Request Model ===
class EmotionInput(BaseModel):
    text: str = Field(..., description="Describe your emotional state, e.g. 'I feel calm and nostalgic'")


# === Response Model ===
class EmotionMusicResponse(BaseModel):
    status: str
    mood: str
    message: str
    device: str | None = None
    playlist: str | None = None


# === Endpoint: Emotion ➜ Music ===
@router.post("/music/from-emotion", response_model=EmotionMusicResponse, tags=["Music"])
async def play_music_from_emotion(input_data: EmotionInput) -> EmotionMusicResponse:
    """
    🎵 Play Music Based on Emotion

    1. Analyzes emotion text via LLM
    2. Maps to closest playlist name from your curated Spotify list
    3. Plays a song randomly from that playlist
    4. Falls back to Spotify search if no direct playlist match
    """
    try:
        return play_music_by_emotion_text(input_data.text)
    except Exception as e:
        return EmotionMusicResponse(
            status="error",
            mood="unknown",
            message=f"Unexpected error: {str(e)}",
            device=None,
            playlist=None
        )