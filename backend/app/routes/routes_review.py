from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models_review
from app.schemas import schemas_review
from app.routes.routes_auth import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas_review.ReviewResponse)
def create_review(
    review: schemas_review.ReviewCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    new_review = models_review.Review(**review.dict(), user_id=current_user.id)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return new_review

@router.get("/{buku_id}", response_model=List[schemas_review.ReviewResponse])
def get_review(buku_id: int, db: Session = Depends(get_db)):
    return db.query(models_review.Review).filter(models_review.Review.buku_id == buku_id).all()
