
from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException
from fastapi import Path

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.ai_service import (
    chat_with_agent
)

from app.core.auth import decode_token


router = APIRouter()


@router.post(
    "/{agent_id}",
    response_model=ChatResponse
)
def chat(
    req: ChatRequest,

    agent_id: int = Path(...),

    authorization: str = Header(...)
):

    # 解析Token
    try:

        token = authorization.split(" ")[1]

    except:

        raise HTTPException(
            status_code=401,
            detail="Token错误"
        )

    # 解码Token
    payload = decode_token(token)

    if not payload:

        raise HTTPException(
            status_code=401,
            detail="Token无效"
        )

    # 获取用户邮箱
    user_email = payload["sub"]

    # 调用Agent聊天
    response = chat_with_agent(
        req.message,
        user_email,
        agent_id
    )

    return {
        "response": response
    }
