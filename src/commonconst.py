# commonconst.py
import os
from dotenv import load_dotenv
import sqlite3
from fastapi import FastAPI, APIRouter, Query
from pydantic import BaseModel
from datetime import datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pathlib import Path

# === Load .env Configuration ===
load_dotenv()

# === Paths ===
BASE_DIR = Path(__file__).resolve().parent.parent
DB_DIR = BASE_DIR / "db"
DB_DIR.mkdir(exist_ok=True)

# Database File Paths
DIARY_DB = DB_DIR / "diary.db"
MOOD_DB = DB_DIR / "mood.db"
MUSIC_DB = DB_DIR / "music.db"
CHAT_DB = DB_DIR / "chat_history.db"

# === Ollama LLM Configuration ===
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# === Spotify API Configuration ===
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
SPOTIFY_SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private"
SPOTIFY_PLAY_ENDPOINT = os.getenv("SPOTIFY_PLAY_ENDPOINT")

# === Telegram Bot Configuration ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# === Lovable Voice Assistant Config (optional) ===
LOVABLE_API_URL = os.getenv("LOVABLE_API_URL")

# === Mood-to-Playlist Mapping ===
MOOD_PLAYLISTS = {
    # 🎉 Happy
    "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",
    "joyful": "spotify:playlist:37i9dQZF1DWYBO1MoTDhZI",
    "excited": "spotify:playlist:37i9dQZF1DX3rxVfibe1L0",

    # 😢 Sad
    "sad": "spotify:playlist:37i9dQZF1DWVrtsSlLKzro",
    "melancholy": "spotify:playlist:37i9dQZF1DX3YSRoSdA634",
    "heartbroken": "spotify:playlist:37i9dQZF1DWZUAeYvs88zc",

    # 😌 Calm
    "calm": "spotify:playlist:37i9dQZF1DWVV27DiNWxkR",
    "relaxed": "spotify:playlist:37i9dQZF1DX3PIPIT6lEg5",
    "peaceful": "spotify:playlist:37i9dQZF1DWUZ5bk6qqDSy",

    # 🎯 Focused
    "focused": "spotify:playlist:37i9dQZF1DX8Uebhn9wzrS",
    "productive": "spotify:playlist:37i9dQZF1DX4sWSpwq3LiO",
    "studying": "spotify:playlist:37i9dQZF1DWWQRwui0ExPn",

    # 😠 Angry
    "angry": "spotify:playlist:37i9dQZF1DWYmmr74INQlb",
    "frustrated": "spotify:playlist:37i9dQZF1DX1tyCD9QhIWF",
    "furious": "spotify:playlist:37i9dQZF1DX3oM43CtKnRV",

    # 🤷 Neutral/Uncertain
    "neutral": "spotify:playlist:37i9dQZF1DX4E3UdUs7fUx",
    "unsure": "spotify:playlist:37i9dQZF1DX4fpCWaHOned"
}
