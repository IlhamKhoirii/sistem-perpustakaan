from pydantic import BaseModel

class KategoriBase(BaseModel):
    nama: str

class KategoriCreate(KategoriBase):
    pass

class KategoriResponse(KategoriBase):
    id: int

    class Config:
        from_attributes = True
