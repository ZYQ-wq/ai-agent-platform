# app/api/user.py

from fastapi import APIRouter, HTTPException, status

from app.schemas.user import (
    RegisterRequest,
    LoginRequest,
    TokenResponse
)

from app.services.user_service import (
    register_service,
    login_service
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# -------------------------
# 注册接口
# -------------------------
@router.post("/register")
def register(req: RegisterRequest):

    try:

        result = register_service(
            req.username,
            req.email,
            req.password
        )

        return {
            "message": result
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器内部错误: {str(e)}"
        )

# -------------------------
# 登录接口
# -------------------------
@router.post(
    "/login",
    response_model=TokenResponse
)
def login(req: LoginRequest):

    try:

        token = login_service(
            req.email,
            req.password
        )

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )

    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"服务器内部错误: {str(e)}"
        )