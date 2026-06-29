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
    success: bool
    stdout: str = ""
    stderr: str = ""
    preview_url:str | None= None

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



# Agent 不再返回代码，而是返回文件变更计划
class FileChange(BaseModel):

    path: str

    action: str

    content: str


from pydantic import BaseModel


class AgentRequest(BaseModel):

    project_id: str

    prompt: str



class ApplyFileChange(BaseModel):
    path: str
    action: str
    content: str = ""

class ApplyChangesRequest(BaseModel):
    project_id: str
    files: list[ApplyFileChange]


class ApplyChangesResponse(BaseModel):
    success: bool

    message: str

class FileChange(BaseModel):

    path: str

    action: str

    content: str


class AgentResponse(BaseModel):

    message: str

    files: list[FileChange]
