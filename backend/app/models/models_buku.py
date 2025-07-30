from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class Buku(Base):
    __tablename__ = "buku"
    id = Column(Integer, primary_key=True, index=True)
    kategori_id = Column(Integer, ForeignKey("kategori.id", ondelete="SET NULL", onupdate="CASCADE"))
    judul = Column(String(150), nullable=False)
    penulis = Column(String(100))
    penerbit = Column(String(100))
    tahun_terbit = Column(String(4))  # gunakan String(4) untuk tahun
    stok = Column(Integer, default=1)
    gambar = Column(String(255))
    created_at = Column(TIMESTAMP)

    kategori = relationship("Kategori")
