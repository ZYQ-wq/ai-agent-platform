from fastapi import APIRouter, Depends, HTTPException
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import chat_with_ai
from app.core.auth import decode_token
from app.core.deps import oauth2_scheme  # 依赖注入

router = APIRouter()

@router.post("/", response_model=ChatResponse)
def chat(
    req: ChatRequest,
    token: str = Depends(oauth2_scheme)
):
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token无效")
    session_id = payload["sub"]

    response = chat_with_ai(req.message, session_id)
    return {"response": response}