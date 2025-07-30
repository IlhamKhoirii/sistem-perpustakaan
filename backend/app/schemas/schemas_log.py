from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class LogBase(BaseModel):
    user_id: Optional[int]
    aktivitas: str

class LogCreate(LogBase):
    pass

class LogResponse(LogBase):
    id: int
    waktu: datetime

    class Config:
        from_attributes = True
