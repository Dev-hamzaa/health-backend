from pydantic import BaseModel
from datetime import date
from typing import Optional

class PatientBase(BaseModel):
    name: str
    dob: date
    email: str
    phone: str
    gender: str
    about: Optional[str] = None
    emergency_contact: str
    medicalRecordNo: str
    address: str
    doctor_id: int

class PatientCreate(PatientBase):
    pass

class PatientOut(PatientBase):
    id: int

    class Config:
        orm_mode = True
