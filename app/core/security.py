from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
    expires = datetime.utcnow() + timedelta(hours=24)
    return jwt.encode({**data, "exp": expires}, settings.SECRET, algorithm="HS256")