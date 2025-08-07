from fastapi import APIRouter ,Depends,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db
from app.services import doctor_service as DoctorService
from app.schema import doctor_schema as DoctorSchema

router = APIRouter(prefix="/doctor", tags=["Doctor"])


@router.post('/')
def create_doctor(doctor: DoctorSchema.DoctorCreate, db: Session = Depends(get_db)):
    created_doctor = DoctorService.create_doctor(db, doctor)
    return {
        "message": "Doctor Created",
        "data": created_doctor
    }


@router.get('/')
def get_doctor_list(db: Session = Depends(get_db)):
    doctor_list=DoctorService.get_doctor_list(db)
    return {
        "message":"Doctors List",
        "data":doctor_list
    }


@router.get("/{id}")
def get_doctor_by_id(id: int, db: Session = Depends(get_db)):
    doctor = DoctorService.get_doctor_by_id(id,db)
    if doctor is None:
        return JSONResponse(status_code=404, content={"message": f"Doctor with ID {id} not found"})
    return {
        "message": f"Doctor with ID {id} retrieved successfully",
        "data": doctor
    }

@router.put("/{id}")
def update_doctor(id: int, updated_data: DoctorSchema.DoctorUpdate, db: Session = Depends(get_db)):
        doctor = DoctorService.update_doctor(id, updated_data,db)
        return {
            "message": f"Doctor with ID {id} updated successfully",
            "data": doctor
        }
    
@router.delete("/{id}")
def delete_doctor(id: int, db: Session = Depends(get_db)):
        doctor = DoctorService.delete_doctor(id,db)
        return {
            "message": f"Doctor with ID {id} deleted successfully"
        }