# from fastapi import APIRouter
# import sqlite3
# import requests
# from dotenv import load_dotenv
# import os
# from router.music_routes import play_music  # direct import

# router = APIRouter()

# # Load environment variables
# load_dotenv()

# # LLM Config
# OLLAMA_URL = "http://localhost:11434/api/generate"
# OLLAMA_MODEL = "llama3"

# # Step 1: Call LLM for mood
# def call_ollama_mood_analyzer(diary_entry: str) -> str:
#     prompt = f"""
#     You are a mood analysis assistant. Given the following diary entry, return ONLY one word from this list:
#     [happy, sad, calm, angry, focused] that best describes the user's mood.

#     Diary Entry: \"{diary_entry}\"

#     Respond with only the word, no explanation.
#     """
#     try:
#         response = requests.post(OLLAMA_URL, json={
#             "model": OLLAMA_MODEL,
#             "prompt": prompt,
#             "stream": False
#         })

#         print("📨 Ollama raw response:", response.text)
#         if response.status_code != 200:
#             return "calm"

#         mood = response.json().get("response", "").strip().lower()
#         print("🧠 Detected mood from LLM:", mood)
#         return mood if mood in ["happy", "sad", "calm", "angry", "focused"] else "calm"

#     except Exception as e:
#         print("⚠️ Ollama error:", e)
#         return "calm"

# # Step 2: Main route
# @router.get("/analyze-mood-and-play")
# async def analyze_mood_and_play_music():
#     # Step 2.1: Get diary entry
#     try:
#         conn = sqlite3.connect("db/jarvis_logs.db")
#         cursor = conn.cursor()
#         cursor.execute("""
#             SELECT id, content FROM logs
#             WHERE category = 'diary'
#             ORDER BY timestamp DESC
#             LIMIT 1
#         """)
#         row = cursor.fetchone()
#         conn.close()
#     except Exception as e:
#         return {"error": f"DB error: {e}"}

#     if not row:
#         return {"error": "No diary entry found."}

#     log_id, diary_entry = row
#     print(f"📘 Diary: {diary_entry}")

#     # Step 2.2: Analyze mood
#     mood = call_ollama_mood_analyzer(diary_entry)

#     # Step 2.3: Log mood
#     try:
#         conn = sqlite3.connect("db/jarvis_logs.db")
#         cursor = conn.cursor()
#         cursor.execute("""
#             INSERT INTO logs (timestamp, category, content)
#             VALUES (datetime('now'), ?, ?)
#         """, ("mood", f"{mood} (from diary log ID {log_id})"))
#         conn.commit()
#         conn.close()
#         print(f"💾 Mood logged: {mood}")
#     except Exception as e:
#         print("⚠️ Log error:", e)

#     # Step 2.4: Play music using internal function
#     try:
#         music_result = await play_music(mood=mood)
#         print("🎵 Playback result:", music_result)
#     except Exception as e:
#         music_result = {"error": f"Playback function failed: {e}"}

#     return {
#         "diary_entry": diary_entry,
#         "mood": mood,
#         "music": music_result
#     }



# router/mood_routes.py
from commonconst import *
from router.interaction.music_vs_mood import *


router = APIRouter()

class MoodRequest(BaseModel):
    diary_entry: str = None

@router.post("/analyze-mood-and-play")
async def analyze_mood_and_play_music(request: MoodRequest):
    diary_entry = request.diary_entry

    if not diary_entry:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, content FROM logs
                WHERE category = 'diary'
                ORDER BY timestamp DESC
                LIMIT 1
            """)
            row = cursor.fetchone()
            conn.close()
            if not row:
                return {"error": "No diary entry found to analyze."}
            _, diary_entry = row
        except Exception as e:
            return {"error": f"Database fetch error: {e}"}
    else:
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO logs (timestamp, category, content)
                VALUES (datetime('now'), 'diary', ?)
            """, (diary_entry,))
            conn.commit()
            conn.close()
        except Exception as e:
            return {"error": f"Failed to log custom diary entry: {e}"}

    mood = analyze_mood_from_diary(diary_entry)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO logs (timestamp, category, content)
            VALUES (datetime('now'), 'mood', ?)
        """, (f"{mood} (from diary entry)",))
        conn.commit()
        conn.close()
    except Exception as e:
        print("⚠️ Error logging mood:", e)

    music_response = play_music_by_mood(mood)

    return {
        "diary_entry": diary_entry,
        "mood": mood,
        "music": music_response
    }