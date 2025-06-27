# src/routes/music_mood_routes.py

from fastapi import APIRouter
from pydantic import BaseModel, Field
from src.interaction.music_mood.music_vs_mood import (
    play_music_by_emotion_text,
    record_music_feedback
)

router = APIRouter()

# === Request & Response Models ===

class EmotionInput(BaseModel):
    text: str = Field(..., description="Describe your emotional state, e.g. 'I feel calm and nostalgic'")
    source: str = Field(default="fastapi", description="Source of interaction (fastapi or telegram)")

class EmotionMusicResponse(BaseModel):
    status: str
    mood: str
    message: str
    device: str | None = None
    playlist: str | None = None
    feedback_prompt: str | None = None

class FeedbackInput(BaseModel):
    user_input: str
    detected_mood: str
    playlist: str
    song_name: str
    user_feedback: str  # should be "yes" or "no"
    source: str = Field(default="fastapi")

class FeedbackResponse(BaseModel):
    result: str

# === Endpoint: Emotion ➜ Music ===
@router.post("/music/from-emotion", response_model=EmotionMusicResponse, tags=["Music"])
async def play_music_from_emotion(input_data: EmotionInput) -> EmotionMusicResponse:
    """
    🎵 Play Music Based on Emotion

    1. Analyzes emotion text via LLM
    2. Maps to closest playlist name from your curated Spotify list
    3. Plays a song randomly from that playlist
    4. Falls back to Spotify search if no direct playlist match
    5. Returns prompt for feedback collection
    """
    try:
        result = play_music_by_emotion_text(input_data.text, source=input_data.source)
        return EmotionMusicResponse(**result)
    except Exception as e:
        return EmotionMusicResponse(
            status="error",
            mood="unknown",
            message=f"Unexpected error: {str(e)}",
            device=None,
            playlist=None
        )

# === Endpoint: Feedback Logging ===
@router.post("/music/feedback", response_model=FeedbackResponse, tags=["Music"])
async def submit_feedback(input_data: FeedbackInput) -> FeedbackResponse:
    """
    ✅ Log user's feedback on emotion-music matching quality
    """
    result = record_music_feedback(
        user_input=input_data.user_input,
        detected_mood=input_data.detected_mood,
        playlist=input_data.playlist,
        song_name=input_data.song_name,
        user_feedback=input_data.user_feedback.lower(),
        source=input_data.source
    )
    return FeedbackResponse(result=result)