from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class LogAktivitas(Base):
    __tablename__ = "log_aktivitas"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="SET NULL", onupdate="CASCADE"))
    aktivitas = Column(String(255))
    waktu = Column(TIMESTAMP)

    user = relationship("User")
