from sqlalchemy import Column, Integer, Float, String, Date
from app.database import Base

class Saving(Base):
    __tablename__ = "savings"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    category = Column(String, default="general")
    notes = Column(String, nullable=True)
