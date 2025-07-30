from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models_log
from app.schemas import schemas_log
from app.routes.routes_auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[schemas_log.LogResponse])
def get_log(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        return []
    return db.query(models_log.LogAktivitas).all()
