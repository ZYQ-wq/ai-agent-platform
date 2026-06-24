from uuid import uuid4
import subprocess
import tempfile
import os
from app.models.agent import Agent


from app.services.sandbox_service import SandboxService

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
    def run_project(
        db: Session,
        project_id: str
    ):

        files = (
            db.query(PluginFile)
            .filter(
                PluginFile.project_id == project_id
            )
            .all()
        )

        with tempfile.TemporaryDirectory() as tmp:

            for file in files:

                file_path = os.path.join(
                    tmp,
                    file.path
                )

                os.makedirs(
                    os.path.dirname(file_path),
                    exist_ok=True
                )

                with open(
                    file_path,
                    "w",
                    encoding="utf-8"
                ) as f:
                    f.write(
                        file.content or ""
                    )

            file_paths = {
                file.path
                for file in files
            }
            if "main.py" in file_paths:

                result = SandboxService.run_python(
                    tmp,
                    "main.py"
                )

            elif "app.py" in file_paths:

                result = SandboxService.run_python(
                    tmp,
                    "app.py"
                )

            elif "index.html" in file_paths:

                result = SandboxService.run_web(
                    tmp
                )

            else:

                return {
                    "success": False,
                    "stdout": "",
                    "stderr":
                        "未找到入口文件"
                }

            return {
                "success": result["success"],
                "stdout": result["logs"],
                "stderr": ""
            }

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
    
    @staticmethod
    def create_file(
        db: Session,
        project_id: str,
        path: str,
        language: str
    ):

        file = PluginFile(
            id=str(uuid4()),
            project_id=project_id,
            path=path,
            language=language,
            content=""
        )

        db.add(file)

        db.commit()

        db.refresh(file)

        return file
    
    @staticmethod
    def delete_file(
        db: Session,
        file_id: str
    ):

        file = (
            db.query(PluginFile)
            .filter(
                PluginFile.id == file_id
            )
            .first()
        )

        if not file:
            return {
                "success": False
            }

        db.delete(file)

        db.commit()

        return {
            "success": True
        }

    @staticmethod
    def rename_file(
        db: Session,
        file_id: str,
        path: str
    ):

        file = (
            db.query(PluginFile)
            .filter(
                PluginFile.id == file_id
            )
            .first()
        )

        if not file:
            return None

        file.path = path

        db.commit()

        db.refresh(file)

        return file
    
    @staticmethod
    def bind_agent(
        db: Session,
        project_id: str,
        agent_id: int | None
    ):

        project = (
            db.query(
                PluginProject
            )
            .filter(
                PluginProject.id == project_id
            )
            .first()
        )

        if not project:
            raise Exception(
                "项目不存在"
            )

        agent = (
            db.query(Agent)
            .filter(
                Agent.id == agent_id
            )
            .first()
        )

        if not agent:
            raise Exception(
                "Agent不存在"
            )

        project.agent_id = agent_id

        db.commit()

        db.refresh(project)

        return project

    @staticmethod
    def apply_changes(
        db: Session,
        project_id: str,
        files: list
    ):
        for item in files:

            path = item.path

            action = item.action

            content = item.content

            file = (
                db.query(
                    PluginFile
                )
                .filter(
                    PluginFile.project_id
                    == project_id,

                    PluginFile.path
                    == path
                )
                .first()
            )

            # create
            if action == "create":

                if not file:

                    db.add(
                        PluginFile(
                            project_id=project_id,
                            path=path,
                            language="plaintext",
                            content=content
                        )
                    )

            # modify
            elif action == "modify":

                if file:

                    file.content = content

            # delete
            elif action == "delete":

                if file:

                    db.delete(file)

        db.commit()

        return {
            "success": True,
            "message": "变更已应用"
        }

