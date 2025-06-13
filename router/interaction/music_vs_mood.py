# router/interaction/music_vs_mood.py
from commonconst import *

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=SPOTIPY_REDIRECT_URI,
    scope=SPOTIFY_SCOPE
))

def analyze_mood_from_diary(diary_entry: str) -> str:
    prompt = f"""
    You are a mood analysis assistant. Given the following diary entry, return ONLY one word from:
    [happy, sad, calm, angry, focused].

    Diary Entry: \"{diary_entry}\"

    Respond with only the word.
    """
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": prompt,
            "stream": False
        })
        mood = response.json().get("response", "").strip().lower()
        return mood if mood in MOOD_PLAYLISTS else "calm"
    except Exception as e:
        print("⚠️ Mood detection failed:", e)
        return "calm"

def play_music_by_mood(mood: str) -> dict:
    try:
        profile = sp.current_user()
        plan = profile.get("product", "None")
        if plan != "premium":
            return {"error": f"Spotify Premium required. Your plan: {plan}"}

        playlist_uri = MOOD_PLAYLISTS.get(mood)
        if not playlist_uri:
            return {"error": f"Unsupported mood '{mood}'."}

        devices = sp.devices()
        if not devices["devices"]:
            return {"error": "No active Spotify devices found."}

        device = next((d for d in devices["devices"] if d["is_active"]), devices["devices"][0])
        sp.start_playback(device_id=device["id"], context_uri=playlist_uri)

        return {
            "status": "playing",
            "mood": mood,
            "device": device["name"]
        }
    except Exception as e:
        return {"error": f"Spotify playback failed: {e}"}