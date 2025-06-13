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

load_dotenv()

# === Paths ===
DB_DIR = "db"
DB_FILE = "jarvis_logs.db"
DB_PATH = os.path.join(DB_DIR, DB_FILE)

# === Spotify Config ===
SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")

# === Spotify OAuth Scope ===
SPOTIFY_SCOPE = "user-read-playback-state user-modify-playback-state user-read-currently-playing user-read-private"

# === Ollama Config ===
OLLAMA_URL = os.getenv("OLLAMA_URL")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")

# === Mood-to-Playlist Mapping ===
MOOD_PLAYLISTS = {
    # Happy
    "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",  # Happy Hits
    "joyful": "spotify:playlist:37i9dQZF1DWYBO1MoTDhZI",  # Have a Great Day!
    "excited": "spotify:playlist:37i9dQZF1DX3rxVfibe1L0",  # Good Vibes

    # Sad
    "sad": "spotify:playlist:37i9dQZF1DWVrtsSlLKzro",  # Sad Songs
    "melancholy": "spotify:playlist:37i9dQZF1DX3YSRoSdA634",  # Life Sucks
    "heartbroken": "spotify:playlist:37i9dQZF1DWZUAeYvs88zc",  # Broken Heart

    # Calm
    "calm": "spotify:playlist:37i9dQZF1DWVV27DiNWxkR",  # Calm Vibes
    "relaxed": "spotify:playlist:37i9dQZF1DX3PIPIT6lEg5",  # Chill Out
    "peaceful": "spotify:playlist:37i9dQZF1DWUZ5bk6qqDSy",  # Peaceful Piano

    # Focused
    "focused": "spotify:playlist:37i9dQZF1DX8Uebhn9wzrS",  # Deep Focus
    "productive": "spotify:playlist:37i9dQZF1DX4sWSpwq3LiO",  # Workday Lounge
    "studying": "spotify:playlist:37i9dQZF1DWWQRwui0ExPn",  # Study Vibes

    # Angry
    "angry": "spotify:playlist:37i9dQZF1DWYmmr74INQlb",  # Rock Hard
    "frustrated": "spotify:playlist:37i9dQZF1DX1tyCD9QhIWF",  # Rage Beats
    "furious": "spotify:playlist:37i9dQZF1DX3oM43CtKnRV",  # All Out Rock

    # Bonus - Neutral/unsure
    "neutral": "spotify:playlist:37i9dQZF1DX4E3UdUs7fUx",  # Mood Booster
    "unsure": "spotify:playlist:37i9dQZF1DX4fpCWaHOned",  # All New Indie
}

# === Spotify Playback Proxy ===
SPOTIFY_PLAY_ENDPOINT = os.getenv("SPOTIFY_PLAY_ENDPOINT")