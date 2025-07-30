from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from jose import JWTError, jwt

from app.database import get_db
from app.models import models_user
from app.schemas import schemas_user
from app.utils import hash_password, verify_password, create_access_token

router = APIRouter()

# JWT Config
SECRET_KEY = "rahasia_perpustakaan"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# ---------------------------
# REGISTER
# ---------------------------
@router.post("/register", response_model=schemas_user.UserResponse)
def register(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    # cek email sudah ada atau belum
    db_user = db.query(models_user.User).filter(models_user.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    # hash password
    hashed_pw = hash_password(user.password)
    new_user = models_user.User(
        nama=user.nama,
        email=user.email,
        password=hashed_pw,
        no_hp=user.no_hp,
        alamat=user.alamat,
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# ---------------------------
# LOGIN
# ---------------------------
@router.post("/login")
def login(form_data: schemas_user.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models_user.User).filter(models_user.User.email == form_data.email).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Email tidak terdaftar")

    if not verify_password(form_data.password, db_user.password):
        raise HTTPException(status_code=400, detail="Password salah")

    # buat token JWT
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email, "role": db_user.role}, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "role": db_user.role,
        "user_id": db_user.id
    }

# ---------------------------
# GET USER LOGIN (Protected)
# ---------------------------
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token tidak valid atau expired",
        headers={"WWW-Authenticate": "Bearer"},
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
