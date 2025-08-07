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
    doctor_id: Optional[int] = None

class PatientCreate(PatientBase):
    pass

class PatientUpdate(BaseModel):
    name: Optional[str]
    dob: Optional[date]
    email: Optional[str]
    phone: Optional[str]
    gender: Optional[str]
    about: Optional[str]
    emergency_contact: Optional[str]
    medicalRecordNo: Optional[str]
    address: Optional[str]
    doctor_id: Optional[int]

class PatientOut(PatientBase):
    id: int

    class Config:
        orm_mode = True
