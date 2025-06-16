# src/routes/mood_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from src.application.mood_analyzer import analyze_mood

router = APIRouter()

class MoodInput(BaseModel):
    text: str

class MoodOutput(BaseModel):
    mood: str

@router.post("/mood/analyze", response_model=MoodOutput)
async def get_mood(input_data: MoodInput):
    mood = analyze_mood(input_data.text)
    return {"mood": mood}