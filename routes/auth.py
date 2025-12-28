"""Authentication routes for the Product Review Engine API."""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, hash_password, verify_password
from database import get_db
from db_models import User

router = APIRouter(prefix="/api/auth", tags=["auth"])


class AuthRegisterRequest(BaseModel):
    email: EmailStr
    password: str


class AuthLoginRequest(BaseModel):
    email: EmailStr
    password: str


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.external_id == email).first()


def create_user(db: Session, email: str, password: str) -> User:
    existing = get_user_by_email(db, email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = User(external_id=email, password_hash=hash_password(password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/register")
async def register(req: AuthRegisterRequest, db: Session = Depends(get_db)):
    user = create_user(db, req.email, req.password)
    token = create_access_token(user_id=user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.external_id},
    }


@router.post("/login")
async def login(req: AuthLoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, req.email)
    if not user or not user.password_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user_id=user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"id": user.id, "email": user.external_id},
    }


@router.get("/me")
async def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.external_id}
