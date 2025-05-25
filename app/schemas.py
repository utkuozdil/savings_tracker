from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import Optional

class SavingBase(BaseModel):
    date: date
    amount: float
    category: Optional[str] = "general"
    notes: Optional[str] = None

class SavingCreate(SavingBase):
    pass

class Saving(SavingBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ErrorResponse(BaseModel):
    error: str
