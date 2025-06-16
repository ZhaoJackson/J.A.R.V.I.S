# src/routes/music_routes.py

from fastapi import APIRouter
from pydantic import BaseModel
from src.application.music_player import play_song_by_name

router = APIRouter()

class SongInput(BaseModel):
    song_name: str

class MusicResponse(BaseModel):
    status: str
    track: str | None = None
    artist: str | None = None
    device: str | None = None
    message: str | None = None

@router.post("/music/play-song", response_model=MusicResponse)
async def play_specific_song(song: SongInput):
    result = play_song_by_name(song.song_name)
    return result