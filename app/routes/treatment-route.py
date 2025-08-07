from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db

router = APIRouter(prefix="/treatment", tags=["Treatments"])

@router.post("/")
def create_treatment():
    return {"message": "Treatment created"}

@router.get("/")
def get_treatment_list(db: Session = Depends(get_db)):
    return JSONResponse(content={"message": "Get treatment list"})

@router.get("/{id}")
def get_treatment_by_id(id: int):
    return {"message": f"Treatment with ID {id} retrieved"}

@router.put("/{id}")
def update_treatment(id: int):
    return {"message": f"Treatment with ID {id} updated"}
