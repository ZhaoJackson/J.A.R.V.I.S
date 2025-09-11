# src/commonconst.py - Clean Configuration

import os
from pathlib import Path
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

# Load environment variables
load_dotenv()

# === Project Paths ===
BASE_DIR = Path(__file__).parent.parent
DB_DIR = BASE_DIR / "db"
BOOK_DIR = BASE_DIR / "src" / "book"
DB_DIR.mkdir(exist_ok=True)

# === Database ===
CHAT_DB = DB_DIR / "chat_history.db"

# === AI Configuration ===
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")
EMBEDDING_MODEL = SentenceTransformer("all-MiniLM-L6-v2")

# === Telegram Bot ===
TELEGRAM_BOT_TOKEN_PHILOSOPHY = os.getenv("TELEGRAM_BOT_TOKEN_PHILOSOPHY", "7781028524:AAG0UZ5lqaeBEGopPQ0V46bcmvihDR-ipq0")

# === Spotify Configuration (Required for real music playback) ===
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET") 
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://localhost:8888/callback")
SPOTIFY_SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing"

# === Spotify Playlists ===
SPOTIFY_PLAYLISTS = {
    "surrealism": os.getenv("SPOTIFY_PLAYLIST_SURREALISM", "0OShHgtBl5wC0pT9Y0ljwQ"),
    "legacy": os.getenv("SPOTIFY_PLAYLIST_LEGACY", "58KWVTWZBrLhx2lqPBDpFM"),
    "reflection": os.getenv("SPOTIFY_PLAYLIST_REFLECTION", "6KCluuukDiva0803j7ZSuF"),
    "memory": os.getenv("SPOTIFY_PLAYLIST_MEMORY", "3RcoPcrCHWtZBQcrPBeXVh"),
    "mindfulness": os.getenv("SPOTIFY_PLAYLIST_MINDFULNESS", "4J9pEg2YdZekZNYeQ51Pum"),
    "resilience": os.getenv("SPOTIFY_PLAYLIST_RESILIENCE", "2garfO6rLVWteexAnupJ8a"),
}

# === Bot Configuration ===
BOT_NAME = os.getenv("BOT_NAME", "JARVIS")
BOT_VERSION = os.getenv("BOT_VERSION", "3.0")

# === Database Configuration ===
EMOTION_LOG_DB = DB_DIR / "emotion_logs.db"
CSV_EXPORT_PATH = DB_DIR / "emotion_history.csv"

# === Default Messages ===
WELCOME_MESSAGE = f"""🤖 Welcome to {BOT_NAME}!

I can help you with emotional support by:
• 📚 Analyzing your emotions
• 💭 Providing philosophical wisdom 
• 🎵 Playing mood-appropriate music

Just tell me how you're feeling!

Commands:
/status - Check system connectivity"""

ERROR_MESSAGE_TEMPLATE = "Sorry, I encountered an error: {error}. Please try again."
SPOTIFY_NOT_CONFIGURED = "❌ Spotify not configured. Music features unavailable."

# === Philosophy Books ===
BOOK_PATHS = {
    "analects": BOOK_DIR / "analects.json",
    "iching": BOOK_DIR / "iching.json", 
    "mencius": BOOK_DIR / "mencius.json",
    "positive_psy": BOOK_DIR / "positive_psy.json",
    "social_psy": BOOK_DIR / "social_psy.json",
    "tao_te_ching": BOOK_DIR / "tao_te_ching.json",
}