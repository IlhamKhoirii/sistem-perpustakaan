from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from enum import Enum

class StatusEnum(str, Enum):
    dipinjam = "dipinjam"
    dikembalikan = "dikembalikan"
    telat = "telat"

class PeminjamanBase(BaseModel):
    user_id: int
    buku_id: int
    tanggal_pinjam: date
    tanggal_jatuh_tempo: date

class PeminjamanCreate(PeminjamanBase):
    pass

class PeminjamanResponse(PeminjamanBase):
    id: int
    tanggal_kembali: date | None = None
    status: StatusEnum
    denda: Decimal

    class Config:
        from_attributes = True
