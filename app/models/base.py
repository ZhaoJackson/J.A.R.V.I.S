from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Use SQLite as default, but allow PostgreSQL via environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./jarvis.db")

# Create async engine
engine = create_async_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# Create async session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

# Dependency
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close() 