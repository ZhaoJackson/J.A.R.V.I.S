# # router/music_routes.py

# from fastapi import APIRouter, Query
# from dotenv import load_dotenv
# import spotipy
# from spotipy.oauth2 import SpotifyOAuth
# import os

# # Load environment variables
# load_dotenv()

# router = APIRouter()

# # Spotify credentials from .env
# SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
# SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
# SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:8888/callback")

# # Add 'user-read-private' to fix Premium detection issue
# SPOTIFY_SCOPE = (
#     "user-read-playback-state user-modify-playback-state "
#     "user-read-currently-playing user-read-private"
# )

# # Spotify client (⚠️ delete .cache file if reauth fails)
# sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
#     client_id=SPOTIPY_CLIENT_ID,
#     client_secret=SPOTIPY_CLIENT_SECRET,
#     redirect_uri=SPOTIPY_REDIRECT_URI,
#     scope=SPOTIFY_SCOPE
# ))

# # Mood-to-playlist mapping
# MOOD_PLAYLISTS = {
#     "happy": "spotify:playlist:37i9dQZF1DXdPec7aLTmlC",
#     "sad": "spotify:playlist:37i9dQZF1DWVrtsSlLKzro",
#     "focused": "spotify:playlist:37i9dQZF1DX8Uebhn9wzrS",
#     "angry": "spotify:playlist:37i9dQZF1DWYmmr74INQlb",
#     "calm": "spotify:playlist:37i9dQZF1DWVV27DiNWxkR"
# }

# @router.get("/music/play")
# async def play_music(mood: str = Query(..., description="Mood like happy, sad, calm, focused, angry")):
#     """
#     Play a Spotify playlist based on detected mood.
#     Requires Spotify Premium and an active Spotify device.
#     """
#     try:
#         # Validate mood
#         playlist_uri = MOOD_PLAYLISTS.get(mood.lower())
#         if not playlist_uri:
#             return {"error": f"Invalid mood '{mood}'. Choose from {list(MOOD_PLAYLISTS.keys())}"}

#         # Validate user is Premium
#         profile = sp.current_user()
#         print("🪪 Spotify Profile:", profile)
#         plan = profile.get("product", None)
#         print("🎧 Plan:", plan)

#         if plan != "premium":
#             return {"error": f"Spotify Premium required. Your plan: {plan}"}

#         # Get active devices
#         devices = sp.devices()
#         print("🎧 Devices:", devices)
#         if not devices["devices"]:
#             return {"error": "No active Spotify devices found. Start playback on a device first."}

#         # Use active device if exists
#         active_device = next((d for d in devices["devices"] if d["is_active"]), devices["devices"][0])
#         device_id = active_device["id"]

#         # Start playback
#         sp.start_playback(device_id=device_id, context_uri=playlist_uri)

#         return {
#             "status": "playing",
#             "mood": mood,
#             "playlist_uri": playlist_uri,
#             "device": active_device["name"]
#         }

#     except spotipy.SpotifyException as se:
#         return {"error": f"Spotify API error: {se}"}
#     except Exception as e:
#         return {"error": f"Unexpected error: {e}"}




# router/music_routes.py

from commonconst import *
from router.interaction.music_vs_mood import *

router = APIRouter()

@router.get("/music/play")
async def play_music(mood: str = Query(..., description="Mood like happy, sad, calm, focused, angry")):
    """
    Triggers Spotify music playback for a given mood.
    Requires Spotify Premium and an active Spotify device.
    """
    return play_music_by_mood(mood)