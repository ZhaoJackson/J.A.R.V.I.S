# src/routes/music_mood_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from src.interaction.music_mood.music_vs_mood import play_music_by_emotional_text

router = APIRouter()

class EmotionInput(BaseModel):
    text: str

class EmotionMusicResponse(BaseModel):
    status: str
    mood: str
    device: str | None = None
    message: str
    playlist: str | None = None

@router.post("/music/from-emotion", response_model=EmotionMusicResponse)
async def play_music_from_emotion(input_data: EmotionInput):
    """
    Accepts emotional text, infers mood using LLM,
    and plays corresponding Spotify playlist.
    """
    result = play_music_by_emotional_text(input_data.text)
    return result