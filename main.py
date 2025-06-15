# main.py
from src.commonconst import *
from src.routes.log_routes import router as log_router
from src.routes.music_routes import router as music_router
from src.routes.mood_routes import router as mood_router
from src.voice_manager.voice_routes import router as voice_router
from src.application.db_manager import *

# === Initialize FastAPI ===
app = FastAPI()

# === Ensure DB Folder Exists ===
os.makedirs(DB_DIR, exist_ok=True)

# === Register Route Modules ===
app.include_router(log_router, prefix="/api")
app.include_router(music_router, prefix="/api")
app.include_router(mood_router, prefix="/api")
app.include_router(voice_router, prefix="/api")

print("🚀 J.A.R.V.I.S FastAPI backend running!")