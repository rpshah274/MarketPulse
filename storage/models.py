from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from storage.database import Base

class TradeRecord(Base):
    __tablename__ = "trades"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    size = Column(Integer)
    exchange = Column(String)
    timestamp = Column(String)
    created_at = Column(DateTime, server_default=func.now())

class IndicatorSnapshot(Base):
    __tablename__ = "indicator_snapshots"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    vwap = Column(Float, nullable=True)
    rsi = Column(Float, nullable=True)
    sma20 = Column(Float, nullable=True)
    ema20 = Column(Float, nullable=True)
    macd = Column(Float, nullable=True)
    bb_upper = Column(Float, nullable=True)
    bb_middle = Column(Float, nullable=True)
    bb_lower = Column(Float, nullable=True)
    created_at = Column(DateTime, server_default=func.now())