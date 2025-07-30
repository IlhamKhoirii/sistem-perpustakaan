from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReviewBase(BaseModel):
    buku_id: int
    user_id: int
    rating: int
    komentar: Optional[str] = None

class ReviewCreate(ReviewBase):
    pass

class ReviewResponse(ReviewBase):
    id: int
    tanggal: datetime

    class Config:
        from_attributes = True
