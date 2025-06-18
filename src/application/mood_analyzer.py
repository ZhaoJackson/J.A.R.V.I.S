# src/application/mood_analyzer.py

import requests
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL

def analyze_mood_profile(text: str) -> dict:
    """
    Uses Ollama LLM to interpret the user's emotional expression.
    Returns a dict: {"mood": <analyzed_mood>} (not bound to predefined categories).
    """

    try:
        prompt = (
            "You are a helpful and emotionally intelligent assistant.\n\n"
            "Your task is to summarize the user's emotional state into a single descriptive word or phrase. "
            "Examples include: 'nostalgic', 'peaceful', 'burnt out', 'motivated', 'anxious', etc.\n\n"
            "Do NOT try to categorize or limit to specific labels. Just give the closest emotion description based on the input.\n"
            "Do not explain your answer. Only respond with the single emotion word or phrase.\n\n"
            f"User Input: \"{text}\"\n\nBest Matching Emotion:"
        )

        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=10
        )

        if not response.ok:
            raise RuntimeError(f"Ollama API error: {response.status_code}")

        result = response.json().get("response", "").strip()
        mood_clean = result.replace('"', '').replace("'", "").strip()

        return {"mood": mood_clean if mood_clean else "calm"}

    except Exception as e:
        print("❌ analyze_mood_profile failed:", e)
        return {"mood": "calm"}