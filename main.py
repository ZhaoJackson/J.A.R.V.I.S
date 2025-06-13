# main.py
from commonconst import *
from router.log_routes import router as log_router
from router.music_routes import router as music_router
from router.mood_routes import router as mood_router

app = FastAPI()

# Ensure the database directory exists
os.makedirs("db", exist_ok=True)

# Initialize the database
def init_db():
    with sqlite3.connect("db/jarvis_logs.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            category TEXT,
            content TEXT
        )
        """)
        conn.commit()

init_db()

# Include route modules
app.include_router(log_router, prefix="/api")
app.include_router(music_router, prefix="/api")
app.include_router(mood_router, prefix="/api")