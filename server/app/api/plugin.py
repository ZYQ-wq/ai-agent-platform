from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

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


@router.post(
    "",
    response_model=PluginProjectResponse
)
def create_project(
    request: PluginProjectCreate,
    db: Session = Depends(get_db)
):
    return PluginService.create_project(
        db=db,
        user_id="demo_user",
        name=request.name,
        description=request.description
    )


@router.get(
    "",
    response_model=list[PluginProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db)
):
    return PluginService.get_projects(
        db=db,
        user_id="demo_user"
    )


@router.get(
    "/{project_id}/files",
    response_model=list[PluginFileResponse]
)
def get_files(
    project_id: str,
    db: Session = Depends(get_db)
):
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
    db: Session = Depends(get_db)
):
    return PluginService.update_file(
        db=db,
        file_id=file_id,
        content=request.content
    )

@router.post(
    "/{project_id}/run",
    response_model=RunProjectResponse
)
def run_project(
    project_id: str,
    db: Session = Depends(get_db)
):
    return PluginService.run_project(
        db=db,
        project_id=project_id
    )

from app.services.codegen_service import (
    CodeGenService
)

@router.post(
    "/generate",
    response_model=GenerateCodeResponse
)
def generate_code(
    request: GenerateCodeRequest
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
    db: Session = Depends(get_db)
):
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
    db: Session = Depends(get_db)
):
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
    db: Session = Depends(get_db)
):
    return PluginService.rename_file(
        db=db,
        file_id=file_id,
        path=request.path
    )

@router.post(
    "/edit",
    response_model=EditCodeResponse
)
def edit_code(
    request: EditCodeRequest
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
    db: Session = Depends(get_db)
):
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
    db: Session = Depends(get_db)
):
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
    db: Session = Depends(get_db)
):

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
    db: Session = Depends(get_db)
):

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
db: Session = Depends(get_db)
):
    return PluginService.apply_changes(
        db=db,
        project_id=request.project_id,
        files=request.files
    )
