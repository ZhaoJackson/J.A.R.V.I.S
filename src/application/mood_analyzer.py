# src/application/mood_analyzer.py
import requests
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL

def analyze_mood_from_text(text: str) -> str:
    """
    Uses a local Ollama LLM to infer mood from text.
    Returns one of the supported moods.
    """
    system_prompt = (
        "You are a mood analysis assistant. Given a diary entry or message, "
        "respond ONLY with the inferred mood. Use one word from the following list:\n"
        "happy, sad, calm, angry, focused, joyful, frustrated, peaceful, excited, heartbroken, studying, relaxed, neutral, unsure."
    )

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": f"{system_prompt}\n\nUser Input: {text}",
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=10)
        response.raise_for_status()
        result = response.json().get("response", "").strip().lower()
        return result.split()[0] if result else "neutral"

    except Exception as e:
        print(f"❌ Mood analysis failed: {e}")
        return "neutral"