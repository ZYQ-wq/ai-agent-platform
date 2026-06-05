# app/schemas/workflow.py

from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime


# 输入变量的值定义（常量或变量引用）
class InputValue(BaseModel):
    kind: str  # "constant" 或 "variable"
    value: Any  # 常量值 或 变量引用字符串，如 "node_id.field_name"


# 工作流节点中的输入变量定义（包含名称、类型和值）
class InputVariable(BaseModel):
    name: str
    type: str
    value: Optional[InputValue] = None  # 允许为空（如开始节点）


# 输出变量定义（仅名称和类型）
class OutputVariable(BaseModel):
    name: str
    type: str


# 工作流节点模式（与前端交互）
class WorkflowNodeSchema(BaseModel):
    node_id: str
    node_type: str
    name: str
    config: Optional[Dict[str, Any]] = None
    inputs: List[InputVariable] = []   # 使用新的 InputVariable 模型
    outputs: List[OutputVariable] = []


# 工作流边
class WorkflowEdgeSchema(BaseModel):
    source_node: str
    target_node: str


# 保存工作流请求
class SaveWorkflowRequest(BaseModel):
    name: str
    description: str = ""
    nodes: List[WorkflowNodeSchema]
    edges: List[WorkflowEdgeSchema]
    workflow_id: Optional[int] = None


# 工作流列表响应
class WorkflowResponse(BaseModel):
    id: int
    name: str
    description: str = "暂无任何描述"
    created_at: datetime

    class Config:
        from_attributes = True


# 工作流详情响应
class WorkflowDetailResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    nodes: List[WorkflowNodeSchema]
    edges: List[WorkflowEdgeSchema]

    class Config:
        from_attributes = True


# 执行工作流请求
class RunWorkflowRequest(BaseModel):
    inputs: Dict[str, Any] = {}