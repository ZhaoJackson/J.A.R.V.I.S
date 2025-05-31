from sqlalchemy import Column, Integer, Float, String, DateTime, Text, Enum
from datetime import datetime
import enum
from .base import Base

class TransactionType(enum.Enum):
    INCOME = "income"
    EXPENSE = "expense"
    INVESTMENT = "investment"
    TRANSFER = "transfer"

class FinanceData(Base):
    __tablename__ = "finance_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    account = Column(String(100), nullable=True)
    balance = Column(Float, nullable=True)
    tags = Column(String(200), nullable=True)
    recurring = Column(String(50), nullable=True)  # daily, weekly, monthly, yearly, none
    investment_type = Column(String(100), nullable=True)  # stocks, bonds, crypto, etc.
    investment_return = Column(Float, nullable=True) 