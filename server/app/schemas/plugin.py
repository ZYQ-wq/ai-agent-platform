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
    description: str | None

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