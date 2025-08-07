from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ReviewBase(BaseModel):
    rating: int
    comment: Optional[str] = None
    doctor_id: Optional[int] = None
    treatment_id: Optional[int] = None
    patient_id: int


class ReviewCreate(ReviewBase):
    pass


class ReviewUpdate(BaseModel):
    rating: Optional[int] = None
    comment: Optional[str] = None


class ReviewOut(ReviewBase):
    id: int
    createdAt: datetime

    class Config:
        orm_mode = True
