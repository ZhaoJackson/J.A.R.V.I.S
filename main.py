# main.py
import os
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# === Project Constants ===
from src.commonconst import DB_DIR

# === Routers ===
from src.routes.log_routes import router as log_router
from src.routes.mood_routes import router as mood_router
from src.routes.music_routes import router as music_router
from src.routes.music_mood_routes import router as music_mood_router
from src.voice_manager.voice_routes import router as voice_router

# === Ensure Database Folder Exists ===
os.makedirs(DB_DIR, exist_ok=True)

# === Initialize FastAPI Application ===
app = FastAPI(
    title="J.A.R.V.I.S. API",
    description="Your mood-aware music assistant powered by FastAPI + Ollama + Spotify",
    version="1.0.0"
)

# === Root Welcome Page ===
@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head><title>J.A.R.V.I.S. API</title></head>
        <body style="font-family:sans-serif; line-height:1.6;">
            <h2>🤖 Welcome to J.A.R.V.I.S. API</h2>
            <p>Your FastAPI server is live and ready.</p>
            <strong>Available Endpoints:</strong>
            <ul>
                <li><code>POST /api/mood/analyze</code> – Analyze mood using Ollama</li>
                <li><code>POST /api/music/play-song</code> – Play a specific Spotify song by name</li>
                <li><code>POST /api/music/from-emotion</code> – Play music based on emotional input</li>
                <li><code>POST /api/log/diary</code> – Log diary entry</li>
                <li><code>POST /api/log/chat</code> – Log chat interaction</li>
                <li><code>POST /api/voice-input</code> – Submit voice input (diary/music mode)</li>
            </ul>
            <p>✨ Explore Swagger at <a href="/docs">/docs</a></p>
        </body>
    </html>
    """

# === Register Route Modules ===
app.include_router(mood_router, prefix="/api")
app.include_router(music_router, prefix="/api")
app.include_router(log_router, prefix="/api")
app.include_router(voice_router, prefix="/api")
app.include_router(music_mood_router, prefix="/api")

print("🚀 J.A.R.V.I.S FastAPI backend running!")