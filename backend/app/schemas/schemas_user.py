from pydantic import BaseModel
from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    anggota = "anggota"

class UserCreate(BaseModel):
    nama: str
    email: str
    password: str
    role: RoleEnum = RoleEnum.anggota

class UserLogin(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    nama: str
    email: str
    role: RoleEnum

    class Config:
        from_attributes = True  # Bisa baca langsung dari SQLAlchemy model
