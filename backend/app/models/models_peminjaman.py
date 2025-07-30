from sqlalchemy import Column, Integer, Date, Enum, ForeignKey, DECIMAL
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class StatusEnum(str, enum.Enum):
    dipinjam = "dipinjam"
    dikembalikan = "dikembalikan"
    telat = "telat"

class Peminjaman(Base):
    __tablename__ = "peminjaman"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    buku_id = Column(Integer, ForeignKey("buku.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    tanggal_pinjam = Column(Date, nullable=False)
    tanggal_jatuh_tempo = Column(Date, nullable=False)
    tanggal_kembali = Column(Date)
    status = Column(Enum(StatusEnum), default=StatusEnum.dipinjam)
    denda = Column(DECIMAL(10, 2), default=0)

    user = relationship("User")
    buku = relationship("Buku")
