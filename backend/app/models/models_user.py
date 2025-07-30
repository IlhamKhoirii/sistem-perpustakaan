from sqlalchemy import Column, Integer, String, Enum, Text, TIMESTAMP
from app.database import Base
import enum

class RoleEnum(str, enum.Enum):
    admin = "admin"
    anggota = "anggota"

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    no_hp = Column(String(15))
    alamat = Column(Text)
    role = Column(Enum(RoleEnum), default=RoleEnum.anggota)
    created_at = Column(TIMESTAMP)
