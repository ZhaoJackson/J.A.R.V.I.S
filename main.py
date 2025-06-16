# main.py

import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from src.commonconst import DB_DIR
from src.application.db_manager import *
from src.routes.log_routes import router as log_router
from src.routes.music_routes import router as music_router
from src.routes.mood_routes import router as mood_router
from src.voice_manager.voice_routes import router as voice_router
from src.routes.music_mood_routes import router as music_mood_router

os.makedirs(DB_DIR, exist_ok=True)

# === Initialize FastAPI ===
app = FastAPI(
    title="J.A.R.V.I.S. API",
    description="Your mood-aware music assistant powered by FastAPI + Ollama + Spotify",
    version="1.0.0"
)

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>J.A.R.V.I.S. API</title></head>
        <body style="font-family:sans-serif;">
            <h2>🤖 Welcome to J.A.R.V.I.S. API</h2>
            <p>Your FastAPI server is running.</p>
            <p>Available endpoints:</p>
            <ul>
                <li><code>POST /api/mood/analyze</code> - Analyze your emotion using Ollama</li>
                <li><code>POST /api/music/play-song</code> - Play a specific Spotify song by name</li>
                <li><code>POST /api/log/diary</code> - Log your diary entry</li>
                <li><code>POST /api/log/chat</code> - Log your chat interaction</li>
                <li><code>POST /api/voice-input</code> - Submit voice to trigger diary/music flow</li>
            </ul>
            <p>Visit <a href="/docs">/docs</a> for Swagger UI</p>
        </body>
    </html>
    """

# === Ensure DB Folder Exists ===
os.makedirs(DB_DIR, exist_ok=True)

# === Register All Route Modules ===
app.include_router(mood_router, prefix="/api")
app.include_router(music_router, prefix="/api")
app.include_router(log_router, prefix="/api")
app.include_router(voice_router, prefix="/api")
app.include_router(music_mood_router, prefix="/api")

print("🚀 J.A.R.V.I.S FastAPI backend running!")