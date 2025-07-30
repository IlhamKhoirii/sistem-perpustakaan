from pydantic import BaseModel
from typing import Optional

class BukuBase(BaseModel):
    judul: str
    penulis: Optional[str] = None
    penerbit: Optional[str] = None
    tahun_terbit: Optional[str] = None
    stok: Optional[int] = 1
    gambar: Optional[str] = None
    kategori_id: Optional[int] = None

class BukuCreate(BukuBase):
    pass

class BukuResponse(BukuBase):
    id: int

    class Config:
        from_attributes = True
