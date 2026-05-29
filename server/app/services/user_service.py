from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.core.database import SessionLocal
from app.core.auth import (
    hash_password,
    verify_password,
    create_access_token
)

# def register_service(username, email, password):

#     db = SessionLocal()

#     exist_user = db.query(User).filter(
#         User.email == email
#     ).first()

#     if exist_user:
#         raise HTTPException(
#             status_code=400,
#             detail="邮箱已存在"
#         )

#     new_user = User(
#         username=username,
#         email=email,
#         password=hash_password(password)
#     )

#     db.add(new_user)

#     db.commit()

#     db.close()

#     return "注册成功"

def register_service(username, email, password):

    db = SessionLocal()

    try:

        new_user = User(
            username=username,
            email=email,
            password=hash_password(password)
        )

        db.add(new_user)

        db.commit()

        return "注册成功"

    except IntegrityError:

        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="用户名或邮箱已存在"
        )

    finally:

        db.close()

def login_service(email, password):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == email
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="用户不存在"
        )
    print(user.password)
    print(type(user.password))
    print(len(user.password))

    if not verify_password(
        password,
        user.password
    ):
        raise HTTPException(
            status_code=400,
            detail="密码错误"
        )

    token = create_access_token({
        "sub": user.email
    })

    return token