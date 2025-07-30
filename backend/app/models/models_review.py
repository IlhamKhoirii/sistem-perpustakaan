from sqlalchemy import Column, Integer, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from app.database import Base

class Review(Base):
    __tablename__ = "review"
    id = Column(Integer, primary_key=True, index=True)
    buku_id = Column(Integer, ForeignKey("buku.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE", onupdate="CASCADE"), nullable=False)
    rating = Column(Integer, nullable=False)
    komentar = Column(Text)
    tanggal = Column(TIMESTAMP)

    buku = relationship("Buku")
    user = relationship("User")
