# src/application/mood_analyzer.py

import requests
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL

def analyze_mood(text: str) -> str:
    """
    Analyzes the mood from input text using the local Ollama LLM.
    """
    prompt = (
        "You are a mood analysis assistant. Given the following text, return ONLY one mood word from:\n"
        "[happy, sad, calm, angry, focused, joyful, frustrated, peaceful, excited, heartbroken, studying, relaxed, neutral, unsure].\n\n"
        f"Text: {text}\nRespond with only the word."
    )

    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        }, timeout=10)
        mood = response.json().get("response", "").strip().lower()
        return mood.split()[0] if mood else "neutral"
    except Exception as e:
        print("❌ LLM mood detection failed:", e)
        return "neutral"