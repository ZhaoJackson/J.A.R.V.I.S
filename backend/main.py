from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import get_settings
from .routers import vision, n8n

app = FastAPI(
    title="JARVIS API",
    description="Backend API for JARVIS - Your Personal Life Assistant",
    version="1.0.0"
)

# Load settings
settings = get_settings()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(vision.router, prefix="/api/vision", tags=["Vision"])
app.include_router(n8n.router, prefix="/api/n8n", tags=["N8N"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to JARVIS API",
        "version": "1.0.0",
        "status": "operational"
    } 