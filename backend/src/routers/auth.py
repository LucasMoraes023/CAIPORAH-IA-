from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..models import User
from ..utils.auth import hash_password, verify_password, create_access_token, decode_access_token
from ..schemas import AuthRegister, AuthLogin, TokenResponse

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post('/register')
async def register(payload: AuthRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.username == payload.username).first()
    if existing:
        raise HTTPException(status_code=400, detail='username already exists')

    user = User(username=payload.username, display_name=payload.display_name or payload.username, password_hash=hash_password(payload.password), role='user')
    db.add(user)
    db.commit()
    db.refresh(user)
    token = create_access_token({'sub': str(user.id), 'username': user.username, 'role': user.role})
    return TokenResponse(access_token=token)


@router.post('/login')
async def login(payload: AuthLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()
    if not user or not user.password_hash:
        raise HTTPException(status_code=400, detail='invalid credentials')

    if not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=400, detail='invalid credentials')

    token = create_access_token({'sub': str(user.id), 'username': user.username, 'role': user.role})
    return TokenResponse(access_token=token)


def get_current_user(authorization: str | None = Header(None), db: Session = Depends(get_db)):
    if authorization is None:
        raise HTTPException(status_code=401, detail='Missing authorization header')

    try:
        scheme, token = authorization.split()
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid authorization header')

    if scheme.lower() != 'bearer':
        raise HTTPException(status_code=401, detail='Invalid auth scheme')

    try:
        payload = decode_access_token(token)
    except Exception:
        raise HTTPException(status_code=401, detail='Invalid token')

    user_id = int(payload.get('sub'))
    db = db or SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail='User not found')
    return user


def require_role(*allowed_roles: str):
    def _dep(current_user: User = Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail='Insufficient permissions')
        return current_user
    return _dep
