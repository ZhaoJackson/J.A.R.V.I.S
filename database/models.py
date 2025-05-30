from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    fitness_data = relationship("FitnessData", back_populates="user")
    calendar_events = relationship("CalendarEvent", back_populates="user")
    books = relationship("Book", back_populates="user")
    github_repos = relationship("GitHubRepo", back_populates="user")
    spotify_playlists = relationship("SpotifyPlaylist", back_populates="user")

class FitnessData(Base):
    __tablename__ = "fitness_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    activity_type = Column(String)
    duration = Column(Integer)  # in minutes
    calories_burned = Column(Integer)
    date = Column(DateTime)
    metadata = Column(JSON)

    user = relationship("User", back_populates="fitness_data")

class CalendarEvent(Base):
    __tablename__ = "calendar_events"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    location = Column(String)
    metadata = Column(JSON)

    user = relationship("User", back_populates="calendar_events")

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    author = Column(String)
    status = Column(String)  # reading, completed, want_to_read
    progress = Column(Integer)  # percentage
    start_date = Column(DateTime)
    completion_date = Column(DateTime)
    notes = Column(String)

    user = relationship("User", back_populates="books")

class GitHubRepo(Base):
    __tablename__ = "github_repos"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    repo_name = Column(String)
    repo_url = Column(String)
    description = Column(String)
    last_updated = Column(DateTime)
    stars = Column(Integer)
    forks = Column(Integer)
    metadata = Column(JSON)

    user = relationship("User", back_populates="github_repos")

class SpotifyPlaylist(Base):
    __tablename__ = "spotify_playlists"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    playlist_id = Column(String, unique=True)
    name = Column(String)
    description = Column(String)
    track_count = Column(Integer)
    last_updated = Column(DateTime)
    metadata = Column(JSON)

    user = relationship("User", back_populates="spotify_playlists") 