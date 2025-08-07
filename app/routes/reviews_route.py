from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from app.schema.reviews import ReviewCreate, ReviewUpdate, ReviewOut
from app.services import reviews_service

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post("/", response_model=ReviewOut)
def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    return reviews_service.create_review(db, review)


@router.get("/{review_id}", response_model=ReviewOut)
def get_review(review_id: int, db: Session = Depends(get_db)):
    review = reviews_service.get_review_by_id(db, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.get("/", response_model=list[ReviewOut])
def list_reviews(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return reviews_service.get_all_reviews(db, skip, limit)


@router.put("/{review_id}", response_model=ReviewOut)
def update_review(review_id: int, review_data: ReviewUpdate, db: Session = Depends(get_db)):
    updated_review = reviews_service.update_review(db, review_id, review_data)
    if not updated_review:
        raise HTTPException(status_code=404, detail="Review not found")
    return updated_review


@router.delete("/{review_id}")
def delete_review(review_id: int, db: Session = Depends(get_db)):
    deleted = reviews_service.delete_review(db, review_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}
