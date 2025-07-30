from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models_user
from app.schemas import schemas_user
from app.routes.routes_auth import get_current_user

router = APIRouter()

# ---------------------------
# Profil user yang login
# ---------------------------
@router.get("/me", response_model=schemas_user.UserResponse)
def get_my_profile(current_user: models_user.User = Depends(get_current_user)):
    return current_user

# ---------------------------
# Admin: Lihat semua user
# ---------------------------
@router.get("/", response_model=List[schemas_user.UserResponse])
def get_all_users(db: Session = Depends(get_db), current_user: models_user.User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa melihat semua user")
    return db.query(models_user.User).all()
