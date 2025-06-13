# router/log_routes.py
from commonconst import *

router = APIRouter()

# Request Schema
class LogEntry(BaseModel):
    category: str
    content: str

@router.post("/log")
async def add_log(entry: LogEntry):
    timestamp = datetime.now().isoformat()
    conn = sqlite3.connect("db/jarvis_logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (timestamp, category, content) VALUES (?, ?, ?)",
                   (timestamp, entry.category, entry.content))
    conn.commit()
    conn.close()
    return {"status": "success", "timestamp": timestamp, "logged": entry.dict()}

@router.get("/logs")
async def get_logs(category: str = None):
    conn = sqlite3.connect("db/jarvis_logs.db")
    cursor = conn.cursor()
    if category:
        cursor.execute("SELECT * FROM logs WHERE category = ?", (category,))
    else:
        cursor.execute("SELECT * FROM logs")
    rows = cursor.fetchall()
    conn.close()
    return {"logs": rows}