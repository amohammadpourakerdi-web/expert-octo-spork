from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from .database import Base
from datetime import datetime

class Melt(Base):
    __tablename__ = "melts"

    id = Column(Integer, primary_key=True, index=True)
    melt_number = Column(String, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    shift = Column(String)
    weight_kg = Column(Float)
    scrap_kg = Column(Float)
    alloy = Column(String)
    notes = Column(Text)
