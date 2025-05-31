from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
import sys

load_dotenv()

# Try to use psycopg2 first, fall back to asyncpg if not available
try:
    import psycopg2
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/jarvis")
except ImportError:
    try:
        import asyncpg
        SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://postgres:postgres@localhost:5432/jarvis")
    except ImportError:
        # Fallback to SQLite if neither PostgreSQL driver is available
        SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./jarvis.db")

# Create engine with appropriate settings
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Enable connection health checks
    pool_recycle=3600,   # Recycle connections after 1 hour
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 