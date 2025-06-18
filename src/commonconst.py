# src/commonconst.py
import os
from dotenv import load_dotenv
from pathlib import Path

# === Load .env Configuration ===
load_dotenv()

# === Project Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(exist_ok=True)

# === Database Paths ===
DIARY_DB = DB_DIR / "diary.db"
MOOD_DB = DB_DIR / "mood.db"
MUSIC_DB = DB_DIR / "music.db"
CHAT_DB = DB_DIR / "chat_history.db"

# === Ollama Model Configuration ===
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# === Spotify API Settings ===
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SPOTIFY_SCOPE = (
    "user-read-playback-state "
    "user-modify-playback-state "
    "user-read-currently-playing "
    "user-read-private "
    "playlist-read-private "
    "playlist-read-collaborative"
)
SPOTIFY_PLAY_ENDPOINT = os.getenv("SPOTIFY_PLAY_ENDPOINT")

# === Telegram Bot Integration ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === Voice Assistant API (Optional) ===
LOVABLE_API_URL = os.getenv("LOVABLE_API_URL")

# === Primary Playlist Mapping (Used by You) ===
SPOTIFY_PLAYLISTS = {
    "nostalgia": "1aB55P67iKNTFxbS4Rzofs",
    "energy": "6cjFaVWqB4ATWj8tT31J1P",
    "focus": "1cFz45Zb9sA9eb8aym60nU",
    "calm": "3e64Rwz2pANOsr2LuglfCq",
    "happy": "3Ddkjjj1BHXEPHnkIfBtfg"
}