from uuid import uuid4
import subprocess
import tempfile
import os
import shutil
from app.models.agent import Agent


from app.services.sandbox_service import SandboxService

from sqlalchemy.orm import Session

from app.models.plugin_project import PluginProject
from app.models.plugin_file import PluginFile


class PluginService:

    _preview_sessions: dict[str, dict] = {}

    @staticmethod
    def _write_project_files(
        files: list[PluginFile],
        target_dir: str
    ):
        for file in files:
            file_path = os.path.join(
                target_dir,
                file.path
            )

            parent_dir = os.path.dirname(file_path)
            if parent_dir:
                os.makedirs(
                    parent_dir,
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

    @staticmethod
    def _file_content(
        files: list[PluginFile],
        path: str
    ) -> str:
        for file in files:
            if file.path == path:
                return (file.content or "").strip()

        return ""

    @staticmethod
    def _find_html_entry(
        file_paths: set[str]
    ) -> str | None:
        if "index.html" in file_paths:
            return "index.html"

        html_files = sorted(
            path
            for path in file_paths
            if path.lower().endswith(".html")
        )

        if html_files:
            return html_files[0]

        return None

    @staticmethod
    def _resolve_run_target(
        files: list[PluginFile]
    ) -> tuple[str, str] | tuple[None, None]:
        file_paths = {
            file.path
            for file in files
        }

        html_entry = PluginService._find_html_entry(
            file_paths
        )
        main_content = PluginService._file_content(
            files,
            "main.py"
        )
        app_content = PluginService._file_content(
            files,
            "app.py"
        )

        if html_entry and not main_content and not app_content:
            return "web", html_entry

        if main_content:
            return "python", "main.py"

        if app_content:
            return "python", "app.py"

        if html_entry:
            return "web", html_entry

        return None, None

    @staticmethod
    def _cleanup_preview(project_id: str):
        session = PluginService._preview_sessions.pop(
            project_id,
            None
        )

        if not session:
            return

        SandboxService.stop_container(
            session["container_id"]
        )

        shutil.rmtree(
            session["workdir"],
            ignore_errors=True
        )

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

        run_type, entry = PluginService._resolve_run_target(
            files
        )

        if not run_type:
            return {
                "success": False,
                "stdout": "",
                "stderr": "未找到入口文件"
            }

        if run_type == "web":
            workdir = tempfile.mkdtemp(
                prefix="plugin_preview_"
            )

            try:
                PluginService._write_project_files(
                    files,
                    workdir
                )

                PluginService._cleanup_preview(
                    project_id
                )

                result = SandboxService.run_web(
                    workdir,
                    entry_path=entry
                )

                PluginService._preview_sessions[
                    project_id
                ] = {
                    "container_id": result["container_id"],
                    "workdir": workdir
                }

                return {
                    "success": True,
                    "stdout": "Web项目启动成功",
                    "stderr": "",
                    "preview_url": result["preview_url"]
                }

            except Exception:
                shutil.rmtree(
                    workdir,
                    ignore_errors=True
                )
                raise

        with tempfile.TemporaryDirectory() as tmp:
            PluginService._write_project_files(
                files,
                tmp
            )

            result = SandboxService.run_python(
                tmp,
                entry
            )

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

        if agent_id is not None:
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
    def _guess_language(path: str) -> str:
        ext = os.path.splitext(path)[1].lower()

        mapping = {
            ".py": "python",
            ".html": "html",
            ".css": "css",
            ".js": "javascript",
            ".ts": "typescript",
            ".json": "json",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".md": "markdown",
        }

        return mapping.get(ext, "plaintext")

    @staticmethod
    def apply_changes(
        db: Session,
        project_id: str,
        files: list
    ):
        applied = 0

        for item in files:
            path = item.path
            action = (item.action or "").strip().lower()
            content = item.content or ""

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

            if action == "delete":
                if file:
                    db.delete(file)
                    applied += 1
                continue

            if action not in ("create", "modify"):
                continue

            if not content.strip():
                continue

            if file:
                file.content = content
                applied += 1
            else:
                db.add(
                    PluginFile(
                        id=str(uuid4()),
                        project_id=project_id,
                        path=path,
                        language=PluginService._guess_language(
                            path
                        ),
                        content=content
                    )
                )
                applied += 1

        db.commit()

        return {
            "success": True,
            "message": f"已应用 {applied} 个变更"
        }

