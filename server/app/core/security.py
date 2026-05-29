# app/core/security.py
from passlib.context import CryptContext
from jose import jwt, JWTError # 导入方式稍微调整一下，直接引入 jwt 模块
from datetime import datetime, timedelta
from .config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    # 使用 jwt.encode 来生成 token
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)