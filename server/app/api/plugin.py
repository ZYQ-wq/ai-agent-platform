from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.services.plugin_service import PluginService
from app.services.codegen_service import CodeGenService

from app.schemas.plugin import (
    PluginProjectCreate,
    PluginFileCreate,
    PluginProjectResponse,
    PluginFileResponse,
    PluginFileUpdate,
    RunProjectResponse
)

from app.schemas.plugin import (
    GenerateCodeRequest,
    GenerateCodeResponse
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