import os
from datetime import datetime, timedelta
from typing import Optional

from passlib.context import CryptContext
import jwt

PWD_CTX = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = os.environ.get('GAMECOPILOT_JWT_SECRET', 'change-me')
JWT_ALGORITHM = 'HS256'


def hash_password(password: str) -> str:
    return PWD_CTX.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    return PWD_CTX.verify(password, hashed)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=8)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
