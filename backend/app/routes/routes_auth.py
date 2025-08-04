from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer

from app.database import get_db
from app.models import models_user
from app.schemas import schemas_user
from app.utils import hash_password, verify_password, create_access_token

router = APIRouter()

SECRET_KEY = "rahasia_perpustakaan"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# ---------------------------
# REGISTER USER
# ---------------------------
@router.post("/register", response_model=schemas_user.UserResponse)
def register(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    # Cek apakah email sudah terdaftar
    db_user = db.query(models_user.User).filter(models_user.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    # Hash password sebelum disimpan
    hashed_pw = hash_password(user.password)

    # Update dict agar password yang disimpan adalah yang sudah di-hash
    user_data = user.dict()
    user_data["password"] = hashed_pw

    new_user = models_user.User(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ---------------------------
# LOGIN USER
# ---------------------------
@router.post("/login")
def login(user: schemas_user.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models_user.User).filter(models_user.User.email == user.email).first()

    # Validasi email & password
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Email atau password salah")

    # Buat token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(
        {"sub": db_user.email, "role": db_user.role},
        access_token_expires
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": db_user.role,
        "user_id": db_user.id
    }

# ---------------------------
# DECODE TOKEN (Dependency)
# ---------------------------
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau expired"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(models_user.User).filter(models_user.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user
