# app/schemas/knowledge.py

from datetime import datetime
from pydantic import BaseModel


# 创建知识库
class KnowledgeCreate(BaseModel):
    name: str
    description: str = ""


# 更新知识库
class KnowledgeUpdate(BaseModel):
    name: str
    description: str = ""


# 返回知识库
class KnowledgeResponse(BaseModel):

    id: int
    name: str
    description: str
    created_at: datetime

    class Config:
        from_attributes = True

class KnowledgeFileResponse(BaseModel):

    id: int

    knowledge_id: int

    file_name: str

    file_path: str

    file_type: str

    created_at: datetime

    class Config:
        from_attributes = True

class KnowledgeChunkResponse(BaseModel):

    id: int

    knowledge_id: int

    file_id: int

    content: str

    index: int

    class Config:
        from_attributes = True

class KnowledgeDetailResponse(BaseModel):

    kb: KnowledgeResponse

    files: list[KnowledgeFileResponse]

    chunks: list[KnowledgeChunkResponse]