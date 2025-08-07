from sqlalchemy.orm import Session
from app.models import Review
from app.schema.reviews import ReviewCreate, ReviewUpdate


def create_review(db: Session, review_data: ReviewCreate):
    review = Review(**review_data.dict())
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_review_by_id(db: Session, review_id: int):
    return db.query(Review).filter(Review.id == review_id).first()


def get_all_reviews(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Review).offset(skip).limit(limit).all()


def update_review(db: Session, review_id: int, review_data: ReviewUpdate):
    review = db.query(Review).filter(Review.id == review_id).first()
    if not review:
        return None
    for field, value in review_data.dict(exclude_unset=True).items():
        setattr(review, field, value)
    db.commit()
    db.refresh(review)
    return review


def delete_review(db: Session, review_id: int):
    review = db.query(Review).filter(Review.id == review_id).first()
    if review:
        db.delete(review)
        db.commit()
        return True
    return False
