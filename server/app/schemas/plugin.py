from pydantic import BaseModel


class PluginFileCreate(BaseModel):
    path: str
    language: str
    content: str


class PluginProjectCreate(BaseModel):
    name: str
    description: str | None = None


class PluginFileResponse(BaseModel):
    id: str
    path: str
    language: str
    content: str


class PluginProjectResponse(BaseModel):

    id: str

    name: str

    description: str | None = None

    agent_id: int | None = None

    runtime: str

    model_config = {
        "from_attributes": True
    }

class PluginFileUpdate(BaseModel):
    content: str

class UpdateFileRequest(BaseModel):
    content: str

class RunProjectResponse(BaseModel):
    stdout: str = ""
    stderr: str = ""
    success: bool

class GenerateCodeRequest(BaseModel):
    project_id: str
    prompt: str

class GenerateCodeResponse(BaseModel):
    content: str

class PluginFileCreate(BaseModel):
    path: str
    language: str = "plaintext"

class RenameFileRequest(BaseModel):
    path: str

# 用于YAML解析
class PluginManifestResponse(
    BaseModel
):

    valid: bool

    data: dict | None = None

    errors: list[str] = []

# AI修改代码
class EditCodeRequest(BaseModel):
    content: str
    prompt: str


class EditCodeResponse(BaseModel):
    content: str

# 多文件操作
class AgentRequest(BaseModel):
    project_id: str
    prompt: str

class AgentResponse(BaseModel):
    files: list[dict]