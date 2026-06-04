from pydantic import BaseModel
from typing import List
from typing import Optional
from typing import Dict
from typing import Any
from datetime import datetime


# =========================
# Node
# =========================

class WorkflowNodeSchema(BaseModel):

    node_id: str

    node_type: str

    name: str

    config: Optional[
        Dict[str, Any]
    ] = None


# =========================
# Edge
# =========================

class WorkflowEdgeSchema(BaseModel):

    source_node: str

    target_node: str


# =========================
# 保存工作流请求
# =========================

class SaveWorkflowRequest(BaseModel):

    name: str

    description: str = ""

    nodes: List[
        WorkflowNodeSchema
    ]

    edges: List[
        WorkflowEdgeSchema
    ]

    # 可选字段，用于更新现有工作流
    workflow_id: Optional[int] = None


# =========================
# 工作流响应
# =========================

class WorkflowResponse(BaseModel):

    id: int

    name: str

    description: str = "暂无任何描述"

    created_at: datetime

    class Config:

        from_attributes = True


# =========================
# 工作流详情响应
# =========================

class WorkflowDetailResponse(BaseModel):

    id: int

    name: str

    nodes: List[
        WorkflowNodeSchema
    ]

    edges: List[
        WorkflowEdgeSchema
    ]

    class Config:

        from_attributes = True

# =========================
# 执行工作流请求
# =========================

class RunWorkflowRequest(BaseModel):

    inputs: Dict[str, Any] = {}