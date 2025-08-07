from fastapi import APIRouter ,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db



# router = APIRouter()
router = APIRouter(prefix="/appointment", tags=["Appointment"])


@router.post('/')
def create_appointment():
    return {"message":"Appointment Created"}


@router.get('/')
def get_appointment_list(db: Session = Depends(get_db)):
    return JSONResponse(content={"message":"get Appointment"})

@router.get("/:id")
def get_appointment_by_id(id: int):
    return {"message": f"Appointment with ID {id} retrieved"}
@router.put("/:id")
def update_appointment(id: int):
    return {"message": f"Appointment with ID {id} updated"}