from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from config.database import get_db

router = APIRouter(prefix="/review", tags=["Reviews"])

@router.post("/")
def create_review():
    return {"message": "Review created"}

@router.get("/")
def get_review_list(db: Session = Depends(get_db)):
    return JSONResponse(content={"message": "Get review list"})

@router.get("/{id}")
def get_review_by_id(id: int):
    return {"message": f"Review with ID {id} retrieved"}

@router.put("/{id}")
def update_review(id: int):
    return {"message": f"Review with ID {id} updated"}
