# src/routes/mood_routes.py
from fastapi import APIRouter
from pydantic import BaseModel
from src.application.mood_analyzer import analyze_mood_from_text

router = APIRouter()

# === Request/Response Models ===
class MoodRequest(BaseModel):
    text: str

class MoodResponse(BaseModel):
    mood: str

# === Route for Mood Analysis ===
@router.post("/analyze-mood", response_model=MoodResponse)
async def analyze_mood(request: MoodRequest):
    """
    Analyze the user's emotional state from free-form text using Ollama LLM.
    Returns a simplified mood label.
    """
    mood = analyze_mood_from_text(request.text)
    return MoodResponse(mood=mood)