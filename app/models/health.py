from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from datetime import datetime
from .base import Base

class HealthData(Base):
    __tablename__ = "health_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    weight = Column(Float, nullable=True)
    sleep_hours = Column(Float, nullable=True)
    exercise_minutes = Column(Integer, nullable=True)
    heart_rate = Column(Integer, nullable=True)
    blood_pressure_systolic = Column(Integer, nullable=True)
    blood_pressure_diastolic = Column(Integer, nullable=True)
    mood = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    water_intake_ml = Column(Integer, nullable=True)
    steps = Column(Integer, nullable=True)
    calories_burned = Column(Integer, nullable=True)
    meditation_minutes = Column(Integer, nullable=True) 