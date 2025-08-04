from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models_kategori
from app.schemas import schemas_kategori
from app.routes.routes_auth import get_current_user

router = APIRouter()

# ---------------------------
# GET semua kategori (user & admin)
# ---------------------------
@router.get("/", response_model=List[schemas_kategori.KategoriResponse])
def get_all_categories(db: Session = Depends(get_db)):
    return db.query(models_kategori.Kategori).all()

# ---------------------------
# Tambah kategori (Admin Only)
# ---------------------------
@router.post("/", response_model=schemas_kategori.KategoriResponse)
def create_category(
    kategori: schemas_kategori.KategoriCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa menambah kategori")
    
    new_category = models_kategori.Kategori(**kategori.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# ---------------------------
# Hapus kategori (Admin Only)
# ---------------------------
@router.delete("/{kategori_id}")
def delete_category(
    kategori_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa menghapus kategori")

    kategori = db.query(models_kategori.Kategori).filter(models_kategori.Kategori.id == kategori_id).first()
    if not kategori:
        raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")

    db.delete(kategori)
    db.commit()
    return {"message": "Kategori berhasil dihapus"}
