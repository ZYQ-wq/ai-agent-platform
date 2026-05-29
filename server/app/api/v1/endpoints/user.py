from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import deps, security
from app.schemas.user import UserCreate, Token, UserOut
from app.services import user_service

router = APIRouter()

@router.post("/register", response_model=UserOut)
def register(user_in: UserCreate, db: Session = Depends(deps.get_db)):
    if user_service.get_user_by_username(db, user_in.username):
        raise HTTPException(status_code=400, detail="用户名已存在")
    if user_service.get_user_by_email(db, user_in.email):
        raise HTTPException(status_code=400, detail="邮箱已注册")
    return user_service.create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(form_data: UserCreate, db: Session = Depends(deps.get_db)):
    # 简化版登录，实际项目建议用 OAuth2PasswordRequestForm
    user = user_service.get_user_by_username(db, form_data.username)
    if not user or not security.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    
    access_token = security.create_jwt_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}