# src/application/db_manager.py - Direct CSV Emotion Logging

import csv
import pandas as pd
from datetime import datetime
from pathlib import Path
from src.commonconst import CSV_EXPORT_PATH

def ensure_csv_exists():
    """Ensure the CSV file exists with proper headers"""
    if not CSV_EXPORT_PATH.exists():
        with open(CSV_EXPORT_PATH, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([
                'Timestamp', 'User Input', 'Detected Emotion', 'Philosophy Book',
                'Music Playlist', 'Music Status', 'Session ID'
            ])

def log_emotion_session(
    user_input: str,
    detected_emotion: str,
    selected_book: str = "none",
    philosopher_response: str = None,
    music_playlist: str = "none",
    music_device: str = "none",
    music_status: str = "none",
    session_id: str = "default"
):
    """Log emotion session directly to CSV file"""
    ensure_csv_exists()
    
    # Append new row to CSV
    with open(CSV_EXPORT_PATH, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            datetime.now().isoformat(),
            user_input,
            detected_emotion,
            selected_book,
            music_playlist,
            music_status,
            session_id
        ])
    
    print(f"📊 Logged to CSV: {detected_emotion} emotion from {session_id}")

def get_emotion_statistics():
    """Get emotion statistics directly from CSV"""
    ensure_csv_exists()
    
    try:
        df = pd.read_csv(CSV_EXPORT_PATH)
        
        if df.empty:
            return {
                "top_emotions": [],
                "top_books": [],
                "recent_activity": [],
                "total_sessions": 0
            }
        
        # Most common emotions
        emotion_counts = df['Detected Emotion'].value_counts().head(10)
        top_emotions = [(emotion, count) for emotion, count in emotion_counts.items()]
        
        # Most used books
        book_counts = df['Philosophy Book'].value_counts()
        top_books = [(book, count) for book, count in book_counts.items()]
        
        # Recent activity
        df['Date'] = pd.to_datetime(df['Timestamp']).dt.date
        daily_counts = df['Date'].value_counts().sort_index().tail(7)
        recent_activity = [(str(date), count) for date, count in daily_counts.items()]
        
        return {
            "top_emotions": top_emotions,
            "top_books": top_books,
            "recent_activity": recent_activity,
            "total_sessions": len(df)
        }
        
    except Exception as e:
        print(f"❌ Error reading CSV statistics: {e}")
        return {
            "top_emotions": [],
            "top_books": [],
            "recent_activity": [],
            "total_sessions": 0
        }

def export_emotions_to_csv():
    """Return the CSV path (already exists as direct logging)"""
    ensure_csv_exists()
    return CSV_EXPORT_PATH