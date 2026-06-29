from fastapi import APIRouter
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import decode_token

from app.models.plugin_project import PluginProject
from app.models.plugin_file import PluginFile

from app.services.plugin_service import PluginService
from app.services.codegen_service import CodeGenService
from app.services.project_agent_service import (
    ProjectAgentService
)

from app.schemas.plugin import (
    PluginProjectCreate,
    PluginFileCreate,
    PluginProjectResponse,
    PluginFileResponse,
    PluginFileUpdate,
    RunProjectResponse,
    RenameFileRequest,
    EditCodeRequest,
    EditCodeResponse,
    AgentRequest,
    AgentResponse,
    ApplyChangesRequest,
    ApplyChangesResponse,
    ApplyFileChange
)

from app.schemas.plugin import (
    GenerateCodeRequest,
    GenerateCodeResponse,
    AgentResponse,
    AgentRequest
)

router = APIRouter(
    prefix="/plugins",
    tags=["Plugins"]
)


def get_user_email(
    authorization: str = Header(...)
) -> str:
    try:
        token = authorization.split(" ")[1]
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Token格式错误"
        )

    payload = decode_token(token)
    return payload["sub"]


def ensure_project_owned(
    db: Session,
    project_id: str,
    user_email: str
) -> PluginProject:
    project = (
        db.query(PluginProject)
        .filter(
            PluginProject.id == project_id,
            PluginProject.user_id == user_email
        )
        .first()
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="项目不存在或无权访问"
        )

    return project


def ensure_file_owned(
    db: Session,
    file_id: str,
    user_email: str
) -> PluginFile:
    file = (
        db.query(PluginFile)
        .join(
            PluginProject,
            PluginFile.project_id == PluginProject.id
        )
        .filter(
            PluginFile.id == file_id,
            PluginProject.user_id == user_email
        )
        .first()
    )

    if not file:
        raise HTTPException(
            status_code=404,
            detail="文件不存在或无权访问"
        )

    return file


@router.post(
    "",
    response_model=PluginProjectResponse
)
def create_project(
    request: PluginProjectCreate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    return PluginService.create_project(
        db=db,
        user_id=user_email,
        name=request.name,
        description=request.description
    )


@router.get(
    "",
    response_model=list[PluginProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    return PluginService.get_projects(
        db=db,
        user_id=user_email
    )


@router.get(
    "/{project_id}/files",
    response_model=list[PluginFileResponse]
)
def get_files(
    project_id: str,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_project_owned(
        db,
        project_id,
        user_email
    )

    return PluginService.get_files(
        db=db,
        project_id=project_id
    )


@router.put(
    "/files/{file_id}",
    response_model=PluginFileResponse
)
def update_file(
    file_id: str,
    request: PluginFileUpdate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_file_owned(
        db,
        file_id,
        user_email
    )

    file = PluginService.update_file(
        db=db,
        file_id=file_id,
        content=request.content
    )

    if not file:
        raise HTTPException(
            status_code=404,
            detail="文件不存在"
        )

    return file

@router.post(
    "/{project_id}/run",
    response_model=RunProjectResponse
)
def run_project(
    project_id: str,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_project_owned(
        db,
        project_id,
        user_email
    )

    return PluginService.run_project(
        db=db,
        project_id=project_id
    )

@router.post(
    "/generate",
    response_model=GenerateCodeResponse
)
def generate_code(
    request: GenerateCodeRequest,
    user_email: str = Depends(get_user_email)
):

    code = CodeGenService.generate_code(
        request.prompt
    )

    return GenerateCodeResponse(
        content=code
    )

@router.post(
    "/{project_id}/files",
    response_model=PluginFileResponse
)
def create_file(
    project_id: str,
    request: PluginFileCreate,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_project_owned(
        db,
        project_id,
        user_email
    )

    return PluginService.create_file(
        db=db,
        project_id=project_id,
        path=request.path,
        language=request.language
    )

@router.delete(
    "/files/{file_id}"
)
def delete_file(
    file_id: str,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_file_owned(
        db,
        file_id,
        user_email
    )

    return PluginService.delete_file(
        db=db,
        file_id=file_id
    )

@router.put(
    "/files/{file_id}/rename",
    response_model=PluginFileResponse
)
def rename_file(
    file_id: str,
    request: RenameFileRequest,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_file_owned(
        db,
        file_id,
        user_email
    )

    file = PluginService.rename_file(
        db=db,
        file_id=file_id,
        path=request.path
    )

    if not file:
        raise HTTPException(
            status_code=404,
            detail="文件不存在"
        )

    return file

@router.post(
    "/edit",
    response_model=EditCodeResponse
)
def edit_code(
    request: EditCodeRequest,
    user_email: str = Depends(get_user_email)
):

    content = CodeGenService.edit_code(
        request.content,
        request.prompt
    )

    return {
        "content": content
    }

@router.put(
    "/{project_id}/agent/{agent_id}",
    response_model=PluginProjectResponse
)
def bind_agent(
    project_id: str,
    agent_id: int,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_project_owned(
        db,
        project_id,
        user_email
    )

    return PluginService.bind_agent(
        db=db,
        project_id=project_id,
        agent_id=agent_id
    )

@router.put(
    "/{project_id}/agent/unbind",
    response_model=PluginProjectResponse
)
def unbind_agent(
    project_id: str,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_project_owned(
        db,
        project_id,
        user_email
    )

    return PluginService.bind_agent(
        db=db,
        project_id=project_id,
        agent_id=None
    )

@router.post(
    "/agent/run",
    response_model=AgentResponse
)
def run_agent(
    request: AgentRequest,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_project_owned(
        db,
        request.project_id,
        user_email
    )

    return (
        ProjectAgentService.run_agent(
            db=db,
            project_id=request.project_id,
            prompt=request.prompt
        )
    )

@router.post(
    "/agent",
    response_model=AgentResponse
)
def agent_chat(
    request: AgentRequest,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_project_owned(
        db,
        request.project_id,
        user_email
    )

    return ProjectAgentService.run_agent(
        db=db,
        project_id=request.project_id,
        prompt=request.prompt
    )

@router.post(
    "/apply",
    response_model=ApplyChangesResponse
)
def apply_changes(
    request: ApplyChangesRequest,
    db: Session = Depends(get_db),
    user_email: str = Depends(get_user_email)
):
    ensure_project_owned(
        db,
        request.project_id,
        user_email
    )

    return PluginService.apply_changes(
        db=db,
        project_id=request.project_id,
        files=request.files
    )
