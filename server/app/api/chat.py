
from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException
from fastapi import Path
from fastapi.responses import StreamingResponse

import json

from app.services.memory_manager import MemoryManager

from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.ai_service import (
    chat_with_agent,
    stream_chat_with_agent,
)

from app.core.auth import decode_token


router = APIRouter()


def _parse_token(authorization: str) -> str:
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token错误"
        )

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token无效"
        )

    return payload["sub"]


def _format_sse(data: dict) -> str:
    return (
        f"data: {json.dumps(data, ensure_ascii=False)}\n\n"
    )


@router.post(
    "/{agent_id}",
    response_model=ChatResponse
)
def chat(
    req: ChatRequest,

    agent_id: int = Path(...),

    authorization: str = Header(...)
):

    user_email = _parse_token(authorization)

    response = chat_with_agent(
        req.message,
        user_email,
        agent_id
    )

    return {
        "response": response
    }


@router.post("/{agent_id}/stream")
def chat_stream(
    req: ChatRequest,
    agent_id: int = Path(...),
    authorization: str = Header(...)
):
    user_email = _parse_token(authorization)

    def event_generator():
        try:
            for event in stream_chat_with_agent(
                req.message,
                user_email,
                agent_id
            ):
                yield _format_sse(event)

        except Exception as exc:
            yield _format_sse({
                "type": "error",
                "message": str(exc)
            })

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        }
    )

@router.get(
    "/history/{agent_id}"
)
def get_chat_history(
    agent_id: int,
    authorization: str = Header(...)
):
    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(
            status_code=401,
            detail="Token错误"
        )
    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Token无效"
        )
    user_email = payload["sub"]

    memory_manager = MemoryManager()

    messages = memory_manager.get_chat_history(
        user_email,
        agent_id
    )

    return messages