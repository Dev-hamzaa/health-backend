from fastapi import APIRouter ,Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db



# router = APIRouter()
router = APIRouter(prefix="/doctor", tags=["Doctor"])


@router.post('/')
def create_doctor():
    return {"message":"user Created"}


@router.get('/')
def get_doctor_list(db: Session = Depends(get_db)):
    return JSONResponse(content={"message":"user Created"})

@router.get("/:id")
def get_doctor_by_id(id: int):
    return {"message": f"Doctor with ID {id} retrieved"}
@router.put("/:id")
def update_doctor(id: int):
    return {"message": f"Doctor with ID {id} updated"}