# src/routes/mood_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from src.application.mood_analyzer import analyze_mood_profile

router = APIRouter()

# === Request/Response Models ===
class MoodInput(BaseModel):
    text: str

class MoodOutput(BaseModel):
    mood: str

# === Route: Analyze Mood ===
@router.post("/mood/analyze", response_model=MoodOutput)
async def analyze_user_mood(input_data: MoodInput) -> MoodOutput:
    result = analyze_mood_profile(input_data.text)
    return MoodOutput(mood=result.get("mood", "neutral"))