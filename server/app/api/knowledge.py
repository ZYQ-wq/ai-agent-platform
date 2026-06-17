from fastapi import APIRouter, UploadFile, File, Header, HTTPException, Path, Body,Form

from app.services.kb_service import (
    create_kb_service,
    upload_kb_service,
    list_kb_service,
    get_kb_service,
    delete_kb_service,
    update_kb_service,
    delete_kb_file_service
)

from app.core.auth import decode_token
from app.schemas.knowledge import KnowledgeCreate,KnowledgeUpdate

from app.schemas.search import SearchRequest
from app.services.search_embedding_service import search_kb_service

router = APIRouter()


# =========================
# 🧠 获取用户ID
# =========================
def get_user_id(authorization: str):

    try:
        token = authorization.split(" ")[1]
    except:
        raise HTTPException(status_code=401, detail="Token格式错误")

    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Token无效")

    return payload["sub"]


# =========================
# 1️⃣ 创建知识库
# =========================
@router.post("/create")
def create_kb(
    data:KnowledgeCreate,
    authorization: str = Header(...)
):

    user_id = get_user_id(authorization)

    kb = create_kb_service(
        user_id=user_id,
        name=data.name,
        description=data.description
    )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "id": kb.id,
            "name": kb.name,
            "description": kb.description
        }
    }


# =========================
# 2️⃣ 上传文件 + 切片（核心）
# =========================
@router.post("/upload/{kb_id}")
def upload_file(
    kb_id: int = Path(...),
    file: UploadFile = File(...),
    authorization: str = Header(...)
):

    user_id = get_user_id(authorization)

    result = upload_kb_service(
        file=file,
        user_id=user_id,
        kb_id=kb_id
    )

    return {
        "code": 0,
        "message": "upload success",
        "data": result
    }


# =========================
# 3️⃣ KB列表
# =========================
@router.get("/list")
def list_kb(authorization: str = Header(...)):

    user_id = get_user_id(authorization)

    kb_list = list_kb_service(user_id)

    return {
        "code": 0,
        "message": "success",
        "data": [
            {
                "id": kb.id,
                "name": kb.name,
                "description": kb.description,
                "created_at": kb.created_at
            }
            for kb in kb_list
        ]
    }


# =========================
# 4️⃣ KB详情（文件列表）
# =========================
@router.get("/{kb_id}")
def get_kb(
    kb_id: int,
    authorization: str = Header(...)
):

    user_id = get_user_id(authorization)

    data = get_kb_service(
        kb_id,
        user_id
    )

    if not data:
        raise HTTPException(
            status_code=404,
            detail="知识库不存在"
        )

    return {
        "code": 0,
        "message": "success",
        "data": {
            "kb": {
                "id": data["kb"].id,
                "name": data["kb"].name,
                "description": data["kb"].description,
                "created_at": data["kb"].created_at
            },
            "files": data["files"]
        }
    }

# =========================
# 5️⃣ 更新KB
# =========================
@router.put("/{kb_id}")
def update_kb(
    kb_id: int,
    data:KnowledgeUpdate,
    authorization: str = Header(...)
):

    user_id = get_user_id(authorization)

    kb = update_kb_service(
        kb_id=kb_id,
        user_id=user_id,
        name=data.name,
        description=data.description
    )

    if not kb:
        raise HTTPException(status_code=404, detail="知识库不存在")

    return {
        "code": 0,
        "message": "update success",
        "data": {
            "id": kb.id,
            "name": kb.name,
            "description": kb.description
        }
    }


# =========================
# 6️⃣ 删除KB（级联）
# =========================
@router.delete("/{kb_id}")
def delete_kb(
    kb_id: int,
    authorization: str = Header(...)
):

    user_id = get_user_id(authorization)

    ok = delete_kb_service(kb_id, user_id)

    if not ok:
        raise HTTPException(status_code=404, detail="知识库不存在")

    return {
        "code": 0,
        "message": "delete success",
        "data": True
    }

@router.delete("/file/{file_id}")
def delete_file(
    file_id: int,
    authorization: str = Header(...)
):

    user_id = get_user_id(authorization)

    ok = delete_kb_file_service(file_id)

    if not ok:
        raise HTTPException(
            status_code=404,
            detail="文件不存在"
        )

    return {
        "code": 0,
        "message": "delete success"
    }

@router.post("/search/{kb_id}")
def search_kb(
    kb_id: int,
    data: SearchRequest,
    authorization: str = Header(...)
):

    user_id = get_user_id(
        authorization
    )

    result = search_kb_service(
        kb_id=kb_id,
        query=data.query,
        top_k=data.top_k
    )

    return {
        "code": 0,
        "message": "success",
        "data": result
    }