from sqlalchemy import Column, Integer, String
from app.database import Base

class Kategori(Base):
    __tablename__ = "kategori"
    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String(50), unique=True, nullable=False)
