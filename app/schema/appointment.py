# schema/appointment.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AppointmentBase(BaseModel):
    scheduledAt: datetime
    status: str
    notes: Optional[str] = None
    doctor_id: Optional[int] = None
    patient_id: Optional[int] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    scheduledAt: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentOut(AppointmentBase):
    id: int

    class Config:
        orm_mode = True
