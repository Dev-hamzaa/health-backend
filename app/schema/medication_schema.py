from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class BaseMedication(BaseModel):
    name:str
    dosage: str
    alergy: Optional[List[str]] = []  
    frequency:str
    prescribedAt:datetime

class MedicationCreate(BaseMedication):
    pass

class MedicationOut(BaseMedication):
    id: int

    class Config:
        from_attributes = True

class MedicationUpdate(BaseModel):
    name: Optional[str]
    dosage: Optional[str]
    alergy: Optional[List[str]]
    frequency: Optional[str]
    prescribedAt: Optional[datetime]
