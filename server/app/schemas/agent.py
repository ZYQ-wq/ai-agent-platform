from pydantic import BaseModel


# 创建Agent请求
class CreateAgentRequest(BaseModel):

    name: str

    description: str

    system_prompt: str


# Agent返回结构
class AgentResponse(BaseModel):

    id: int

    name: str

    description: str

    system_prompt: str

    class Config:

        from_attributes = True

