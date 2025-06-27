# src/application/db_manager.py

import sqlite3
from datetime import datetime
from src.commonconst import DIARY_DB, MOOD_DB, MUSIC_DB, CHAT_DB

# === Base DB Init Function ===
def init_db(path: str, schema: str):
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    cursor.execute(schema)
    conn.commit()
    conn.close()

# === Diary Entry Logging ===
def log_diary_entry(content: str):
    schema = """
    CREATE TABLE IF NOT EXISTS diary (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        content TEXT
    )
    """
    init_db(DIARY_DB, schema)
    with sqlite3.connect(DIARY_DB) as conn:
        conn.execute(
            "INSERT INTO diary (timestamp, content) VALUES (?, ?)",
            (datetime.now().isoformat(), content)
        )
        conn.commit()

# === Mood Analysis Logging ===
def log_mood_analysis(input_text: str, mood: str):
    schema = """
    CREATE TABLE IF NOT EXISTS mood_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user_input TEXT,
        detected_mood TEXT
    )
    """
    init_db(MOOD_DB, schema)
    with sqlite3.connect(MOOD_DB) as conn:
        conn.execute(
            "INSERT INTO mood_logs (timestamp, user_input, detected_mood) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), input_text, mood)
        )
        conn.commit()

# === Music Playback Logging ===
def log_music_playback(mood: str, playlist_uri: str, device: str):
    schema = """
    CREATE TABLE IF NOT EXISTS music_playback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        mood TEXT,
        playlist_uri TEXT,
        device TEXT
    )
    """
    init_db(MUSIC_DB, schema)
    with sqlite3.connect(MUSIC_DB) as conn:
        conn.execute(
            "INSERT INTO music_playback (timestamp, mood, playlist_uri, device) VALUES (?, ?, ?, ?)",
            (datetime.now().isoformat(), mood, playlist_uri, device)
        )
        conn.commit()

# === Optional: Log Full Track-to-Mood Matching Scores ===
def log_music_play(
    mood_text: str,
    song_name: str,
    artist: str,
    playlist: str,
    similarity: float,
    valence: float,
    energy: float,
    acousticness: float
):
    schema = """
    CREATE TABLE IF NOT EXISTS music_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        mood_text TEXT,
        song_name TEXT,
        artist TEXT,
        playlist TEXT,
        similarity REAL,
        valence REAL,
        energy REAL,
        acousticness REAL
    )
    """
    init_db(MUSIC_DB, schema)
    with sqlite3.connect(MUSIC_DB) as conn:
        conn.execute("""
            INSERT INTO music_logs (
                timestamp, mood_text, song_name, artist, playlist,
                similarity, valence, energy, acousticness
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().isoformat(),
            mood_text, song_name, artist, playlist,
            similarity, valence, energy, acousticness
        ))
        conn.commit()

# === Chat History Logging ===
def log_chat_message(source: str, message: str):
    schema = """
    CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        source TEXT,
        message TEXT
    )
    """
    init_db(CHAT_DB, schema)
    with sqlite3.connect(CHAT_DB) as conn:
        conn.execute(
            "INSERT INTO chat_history (timestamp, source, message) VALUES (?, ?, ?)",
            (datetime.now().isoformat(), source, message)
        )
        conn.commit()

# === Feedback Logging ===
def log_music_feedback(
    user_input: str,
    detected_mood: str,
    playlist: str,
    song_name: str,
    user_feedback: str,
    source: str
):
    schema = """
    CREATE TABLE IF NOT EXISTS feedback_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user_input TEXT,
        detected_mood TEXT,
        playlist TEXT,
        song_name TEXT,
        user_feedback TEXT,
        source TEXT
    )
    """
    init_db(MUSIC_DB, schema)
    with sqlite3.connect(MUSIC_DB) as conn:
        conn.execute(
            """
            INSERT INTO feedback_logs (
                timestamp, user_input, detected_mood,
                playlist, song_name, user_feedback, source
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now().isoformat(),
                user_input,
                detected_mood,
                playlist,
                song_name,
                user_feedback,
                source
            )
        )
        conn.commit()