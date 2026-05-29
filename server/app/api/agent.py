
from fastapi import APIRouter
from fastapi import Header
from fastapi import HTTPException

from typing import List

from app.schemas.agent import (
    CreateAgentRequest,
    AgentResponse
)

from app.services.agent_service import (
    create_agent_service,
    get_agents_service
)

from app.core.auth import decode_token


router = APIRouter()


# 创建Agent
@router.post(
    "/create",
    response_model=AgentResponse
)
def create_agent(
    req: CreateAgentRequest,
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

    agent = create_agent_service(
        user_email,
        req.name,
        req.description,
        req.system_prompt
    )

    return agent


# 获取我的Agent
@router.get(
    "/my",
    response_model=List[AgentResponse]
)
def get_my_agents(
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

    agents = get_agents_service(
        user_email
    )

    return agents
