from uuid import uuid4

from sqlalchemy.orm import Session

from app.models.plugin_project import PluginProject
from app.models.plugin_file import PluginFile


class PluginService:

    @staticmethod
    def create_project(
        db: Session,
        user_id: str,
        name: str,
        description: str | None = None
    ):

        project = PluginProject(
            id=str(uuid4()),
            user_id=user_id,
            name=name,
            description=description
        )

        db.add(project)

        db.flush()

        default_files = [

            PluginFile(
                id=str(uuid4()),
                project_id=project.id,
                path="main.py",
                language="python",
                content=""
            ),

            PluginFile(
                id=str(uuid4()),
                project_id=project.id,
                path="plugin.yaml",
                language="yaml",
                content=""
            ),

            PluginFile(
                id=str(uuid4()),
                project_id=project.id,
                path="README.md",
                language="markdown",
                content=""
            )

        ]

        db.add_all(default_files)

        db.commit()

        db.refresh(project)

        return project
    
    @staticmethod
    def get_projects(
        db: Session,
        user_id: str
    ):

        return (
            db.query(
                PluginProject
            )
            .filter(
                PluginProject.user_id == user_id
            )
            .all()
        )

    @staticmethod
    def get_files(
        db: Session,
        project_id: str
    ):

        return (
            db.query(
                PluginFile
            )
            .filter(
                PluginFile.project_id == project_id
            )
            .all()
        )

    @staticmethod
    def update_file(
        db: Session,
        file_id: str,
        content: str
    ):

        file = (
            db.query(
                PluginFile
            )
            .filter(
                PluginFile.id == file_id
            )
            .first()
        )

        if not file:
            return None

        file.content = content

        db.commit()

        db.refresh(file)

        return file