from fastapi import FastAPI
from app.database import Base, engine

from app.routes import (
    routes_auth, routes_user, routes_buku, routes_peminjaman,
    routes_review, routes_denda, routes_log, routes_kategori
)

from app.models import models_user, models_kategori, models_buku, models_peminjaman, models_review, models_log, models_denda

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Sistem Peminjaman Buku")

app.include_router(routes_auth.router, prefix="/auth", tags=["Auth"])
app.include_router(routes_user.router, prefix="/users", tags=["Users"])
app.include_router(routes_buku.router, prefix="/buku", tags=["Buku"])
app.include_router(routes_kategori.router, prefix="/kategori", tags=["Kategori"])
app.include_router(routes_peminjaman.router, prefix="/peminjaman", tags=["Peminjaman"])
app.include_router(routes_review.router, prefix="/review", tags=["Review"])
app.include_router(routes_denda.router, prefix="/denda", tags=["Denda"])
app.include_router(routes_log.router, prefix="/log", tags=["Log Aktivitas"])
