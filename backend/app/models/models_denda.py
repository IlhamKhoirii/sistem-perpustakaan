from sqlalchemy import Column, Integer, DECIMAL
from app.database import Base

class Denda(Base):
    __tablename__ = "denda"
    id = Column(Integer, primary_key=True, index=True)
    jumlah_per_hari = Column(DECIMAL(10, 2), nullable=False)
