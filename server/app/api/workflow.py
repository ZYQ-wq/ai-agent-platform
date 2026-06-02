from fastapi import APIRouter, Header, HTTPException, Path
from typing import List

from app.schemas.workflow import (
    SaveWorkflowRequest,
    WorkflowResponse,
    WorkflowDetailResponse
)

from app.services.workflow_service import (
    save_workflow_service,
    get_workflows_service,
    get_workflow_detail_service,
    delete_workflow_service
)

from app.core.auth import decode_token

router = APIRouter()


# 保存工作流
@router.post(
    "/save",
    response_model=dict
)
def save_workflow(
    req: SaveWorkflowRequest,
    authorization: str = Header(...)
):

    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Token错误")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token无效")

    user_email = payload["sub"]

    return save_workflow_service(user_email, req)


# 获取我的工作流列表
@router.get(
    "/my",
    response_model=List[WorkflowResponse]
)
def get_my_workflows(
    authorization: str = Header(...)
):

    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Token错误")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token无效")

    user_email = payload["sub"]

    return get_workflows_service(user_email)


# 获取工作流详情
@router.get(
    "/{workflow_id}",
    response_model=WorkflowDetailResponse
)
def get_workflow(
    workflow_id: int = Path(...),
    authorization: str = Header(...)
):

    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Token错误")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token无效")

    user_email = payload["sub"]

    return get_workflow_detail_service(workflow_id, user_email)


# 删除工作流
@router.delete(
    "/{workflow_id}",
    response_model=dict
)
def delete_workflow(
    workflow_id: int = Path(...),
    authorization: str = Header(...)
):

    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Token错误")

    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token无效")

    user_email = payload["sub"]

    return delete_workflow_service(workflow_id, user_email)