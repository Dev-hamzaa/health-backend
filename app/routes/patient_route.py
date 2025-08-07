from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.schema.patient import PatientCreate, PatientOut
from app.models import Patient
from config.deps import get_db

router = APIRouter(prefix="/patients", tags=["Patients"])

@router.post("/", response_model=PatientOut)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    db_patient = Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
