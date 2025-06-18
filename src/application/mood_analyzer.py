# src/application/mood_analyzer.py
import requests
from src.commonconst import OLLAMA_URL, OLLAMA_MODEL

def analyze_mood_profile(text: str) -> dict:
    """
    Uses Ollama LLM to classify emotion into one of the 5 predefined playlists.
    Returns a dict: {"mood": <playlist_name>} where the name matches closest.
    """

    try:
        prompt = (
            "You are a helpful and emotionally intelligent assistant.\n\n"
            "Your task is to analyze the user's emotional expression and match it to the most suitable mood category "
            "from the following list of playlist names:\n"
            "- Nostalgia\n- Energy\n- Focus\n- Calm\n- Happy\n\n"
            "Only respond with ONE exact category name from the list above, based on your best interpretation.\n"
            "Do not explain your answer. Just respond with the one-word category.\n\n"
            f"User Input: \"{text}\"\n\nBest Matching Category:"
        )

        response = requests.post(
            OLLAMA_URL,
            json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
            timeout=10
        )
        if not response.ok:
            raise RuntimeError(f"Ollama API error: {response.status_code}")

        result = response.json().get("response", "").strip()
        mood_clean = result.replace('"', '').replace("'", "").strip().capitalize()

        return {"mood": mood_clean if mood_clean in [
            "Nostalgia", "Energy", "Focus", "Calm", "Happy"
        ] else "Calm"}

    except Exception as e:
        print("❌ analyze_mood_profile failed:", e)
        return {"mood": "Calm"}