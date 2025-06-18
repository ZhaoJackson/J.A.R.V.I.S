# src/routes/music_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from src.application.music_player import search_and_play_by_keyword

router = APIRouter()

# === Request/Response Models ===
class SongInput(BaseModel):
    song_name: str

class MusicResponse(BaseModel):
    status: str
    track: str | None = None
    artist: str | None = None
    device: str | None = None
    message: str | None = None

# === Route: Play Song by Name ===
@router.post("/music/play-song", response_model=MusicResponse)
async def play_specific_song(song: SongInput):
    """
    Search and play a specific Spotify song by name.

    Example request body:
    {
        "song_name": "Blinding Lights"
    }

    Example response:
    {
        "status": "success",
        "track": "Blinding Lights",
        "artist": "The Weeknd",
        "device": "Zichen's iPhone",
        "message": "🎵 Now playing on your active device"
    }
    """
    return search_and_play_by_keyword(song.song_name)