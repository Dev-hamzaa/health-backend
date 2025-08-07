from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.schema.patient import PatientCreate, PatientOut, PatientUpdate
from config.database import get_db
from app.services.patient_service import (
    create_patient_service,
    get_patient_service,
    update_patient_service,
    delete_patient_service,
)

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientOut, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    return create_patient_service(db, patient)

@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    return get_patient_service(db, patient_id)

@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(patient_id: int, patient_update: PatientUpdate, db: Session = Depends(get_db)):
    return update_patient_service(db, patient_id, patient_update)

@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    delete_patient_service(db, patient_id)
