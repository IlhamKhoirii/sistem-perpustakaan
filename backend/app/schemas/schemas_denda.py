from pydantic import BaseModel
from decimal import Decimal

class DendaBase(BaseModel):
    jumlah_per_hari: Decimal

class DendaCreate(DendaBase):
    pass

class DendaResponse(DendaBase):
    id: int

    class Config:
        from_attributes = True
