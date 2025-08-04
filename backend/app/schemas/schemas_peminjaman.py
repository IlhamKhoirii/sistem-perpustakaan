from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from enum import Enum

class StatusEnum(str, Enum):
    dipinjam = "dipinjam"
    dikembalikan = "dikembalikan"
    telat = "telat"

class PeminjamanBase(BaseModel):
    buku_id: int
    tanggal_pinjam: date
    tanggal_jatuh_tempo: date | None = None  # optional, bisa diisi otomatis

class PeminjamanCreate(PeminjamanBase):
    pass

class PeminjamanResponse(PeminjamanBase):
    id: int
    user_id: int
    tanggal_kembali: date | None = None
    status: StatusEnum
    denda: Decimal

    class Config:
        from_attributes = True
