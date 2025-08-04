from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from typing import List

from app.database import get_db
from app.models import models_peminjaman, models_buku
from app.schemas import schemas_peminjaman
from app.routes.routes_auth import get_current_user

router = APIRouter()

# ---------------------------
# User pinjam buku
# ---------------------------
@router.post("/", response_model=schemas_peminjaman.PeminjamanResponse)
def pinjam_buku(
    peminjaman: schemas_peminjaman.PeminjamanCreate, 
    db: Session = Depends(get_db), 
    current_user = Depends(get_current_user)
):
    buku = db.query(models_buku.Buku).filter(models_buku.Buku.id == peminjaman.buku_id).first()
    if not buku or buku.stok < 1:
        raise HTTPException(status_code=400, detail="Buku tidak tersedia")
    
    buku.stok -= 1

    # Tentukan tanggal jatuh tempo otomatis (misalnya 7 hari dari pinjam)
    tanggal_jatuh_tempo = peminjaman.tanggal_pinjam + timedelta(days=7)

    new_peminjaman = models_peminjaman.Peminjaman(
        buku_id=peminjaman.buku_id,
        tanggal_pinjam=peminjaman.tanggal_pinjam,
        tanggal_jatuh_tempo=tanggal_jatuh_tempo,
        user_id=current_user.id
    )

    db.add(new_peminjaman)
    db.commit()
    db.refresh(new_peminjaman)
    return new_peminjaman

# ---------------------------
# User lihat history peminjaman
# ---------------------------
@router.get("/me", response_model=List[schemas_peminjaman.PeminjamanResponse])
def get_my_peminjaman(
    db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    return db.query(models_peminjaman.Peminjaman).filter(models_peminjaman.Peminjaman.user_id == current_user.id).all()

# ---------------------------
# Admin lihat semua peminjaman
# ---------------------------
@router.get("/", response_model=List[schemas_peminjaman.PeminjamanResponse])
def get_all_peminjaman(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa melihat semua peminjaman")
    return db.query(models_peminjaman.Peminjaman).all()

# ---------------------------
# User kembalikan buku
# ---------------------------
@router.put("/{peminjaman_id}")
def kembalikan_buku(
    peminjaman_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)
):
    peminjaman = db.query(models_peminjaman.Peminjaman).filter(models_peminjaman.Peminjaman.id == peminjaman_id).first()
    if not peminjaman:
        raise HTTPException(status_code=404, detail="Data peminjaman tidak ditemukan")
    peminjaman.tanggal_kembali = date.today()
    peminjaman.status = "dikembalikan"
    buku = db.query(models_buku.Buku).filter(models_buku.Buku.id == peminjaman.buku_id).first()
    buku.stok += 1
    db.commit()
    return {"message": "Buku berhasil dikembalikan"}
