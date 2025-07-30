from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import models_buku
from app.schemas import schemas_buku
from app.routes.routes_auth import get_current_user

router = APIRouter()

# ---------------------------
# Semua user bisa lihat daftar buku
# ---------------------------
@router.get("/", response_model=List[schemas_buku.BukuResponse])
def get_all_books(db: Session = Depends(get_db)):
    return db.query(models_buku.Buku).all()

# ---------------------------
# Admin tambah buku
# ---------------------------
@router.post("/", response_model=schemas_buku.BukuResponse)
def create_book(
    buku: schemas_buku.BukuCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa menambah buku")
    new_book = models_buku.Buku(**buku.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# ---------------------------
# Admin hapus buku
# ---------------------------
@router.delete("/{buku_id}")
def delete_book(
    buku_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa menghapus buku")
    book = db.query(models_buku.Buku).filter(models_buku.Buku.id == buku_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Buku tidak ditemukan")
    db.delete(book)
    db.commit()
    return {"message": "Buku berhasil dihapus"}
