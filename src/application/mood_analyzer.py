# src/application/mood_analyzer.py

import requests
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL

def analyze_emotion(text: str) -> str:
    """Analyze emotion from text using Ollama and return the emotion string"""
    prompt = f"Analyze this emotion in one word: '{text}'. Respond with only the emotion word."
    
    response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=30
    )
    
    if response.ok:
        emotion = response.json().get("response", "calm").strip().replace('"', '').replace("'", "")
        return emotion if emotion else "calm"
    return "calm"