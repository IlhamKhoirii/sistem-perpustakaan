from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models_denda
from app.schemas import schemas_denda
from app.routes.routes_auth import get_current_user

router = APIRouter()

# Admin atur denda
@router.post("/", response_model=schemas_denda.DendaResponse)
def set_denda(
    denda: schemas_denda.DendaCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa mengatur denda")
    new_denda = models_denda.Denda(**denda.dict())
    db.add(new_denda)
    db.commit()
    db.refresh(new_denda)
    return new_denda

# Lihat aturan denda
@router.get("/", response_model=List[schemas_denda.DendaResponse])
def get_denda(db: Session = Depends(get_db)):
    return db.query(models_denda.Denda).all()
