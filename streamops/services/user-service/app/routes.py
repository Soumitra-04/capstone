from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import bcrypt

from app.database import get_db
from app.models import User
from app.schemas import UserCreate, UserResponse, UserLogin, LoginResponse, HealthResponse

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "user-service"}


@router.post("/users/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    existing = db.query(User).filter(
        (User.username == user.username) | (User.email == user.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/users/login", response_model=LoginResponse)
def login_user(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login a user and return their id and username."""
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not bcrypt.checkpw(credentials.password.encode('utf-8'), user.password_hash.encode('utf-8')):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"id": user.id, "username": user.username, "message": "Login successful"}


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user details by ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/users", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db)):
    """List all users."""
    return db.query(User).all()
