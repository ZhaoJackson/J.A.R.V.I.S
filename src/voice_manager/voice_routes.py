from fastapi import APIRouter, Request
from src.application.mood_analyzer import *
from src.application.music_player import play_song_by_uri
from src.commonconst import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
import requests

router = APIRouter()

@router.post("/voice-input")
async def handle_voice_input(request: Request):
    try:
        data = await request.json()
        print(f"📥 Received data: {data}")
        
        user_input = data.get("text", "")
        if not user_input:
            return {"error": "Missing 'text' in request body."}
        
        # 1. Mood analysis
        mood = analyze_mood_from_text(user_input)
        print(f"🧠 Analyzed mood: {mood}")

        # 2. Trigger Spotify
        result = play_music_by_mood(mood)
        print(f"🎵 Music result: {result}")

        # 3. Telegram message
        send_to_telegram_log(user_input, mood, result)
        print("📨 Telegram message sent.")

        # 4. Voice assistant response
        return {
            "response": f"I sense you're feeling {mood}. I'm playing a playlist to match that mood."
        }

    except Exception as e:
        print(f"❌ ERROR in voice-input handler: {e}")
        return {"error": str(e)}

def send_to_telegram_log(user_input: str, mood: str, result: dict):
    message = (
        f"🎙 Voice Log: '{user_input}'\n"
        f"Detected Mood: {mood}\n"
        f"Music: {result.get('status', result.get('error', 'unknown'))}"
    )
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    requests.post(url, json=payload)