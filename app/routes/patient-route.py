from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db

router = APIRouter(prefix="/patient", tags=["Patients"])

@router.post("/")
def create_patient():
    return {"message": "Patient created"}

@router.get("/")
def get_patient_list(db: Session = Depends(get_db)):
    return JSONResponse(content={"message": "Get patient list"})

@router.get("/{id}")
def get_patient_by_id(id: int):
    return {"message": f"Patient with ID {id} retrieved"}

@router.put("/{id}")
def update_patient(id: int):
    return {"message": f"Patient with ID {id} updated"}
