import json

from sqlalchemy.orm import Session

from openai import OpenAI

from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL
)

from app.models.agent import Agent
from app.models.plugin_project import PluginProject
from app.models.plugin_file import PluginFile


client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


class ProjectAgentService:

    @staticmethod
    def run_agent(
        db: Session,
        project_id: str,
        prompt: str
    ):

        # -------------------
        # 查询项目
        # -------------------

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

        # -------------------
        # 查询Agent
        # -------------------

        if not project.agent_id:
            raise Exception(
                "项目未绑定Agent"
            )

        agent = (
            db.query(
                Agent
            )
            .filter(
                Agent.id == project.agent_id
            )
            .first()
        )

        if not agent:
            raise Exception(
                "Agent不存在"
            )

        # -------------------
        # 获取全部文件
        # -------------------

        files = (
            db.query(
                PluginFile
            )
            .filter(
                PluginFile.project_id
                == project.id
            )
            .all()
        )

        # -------------------
        # 构造上下文
        # -------------------

        project_context = ""

        for file in files:

            content = (
                file.content or ""
            )

            # 防止超长
            content = content[:8000]

            project_context += f"""

FILE:
{file.path}

CONTENT:
{content}

================================

"""

        # -------------------
        # Agent Prompt
        # -------------------

        final_prompt = f"""
你是一个软件开发Agent。

Agent配置：

{agent.system_prompt}

下面是项目全部文件：

{project_context}

用户需求：

{prompt}

请分析项目。

决定哪些文件需要修改。

返回JSON格式：

{{
    "files":[
        {{
            "path":"main.py",
            "content":"完整文件内容"
        }}
    ]
}}

不要返回Markdown。
不要返回解释。
只返回JSON。
"""

        # -------------------
        # 调用大模型
        # -------------------

        resp = (
            client.chat.completions.create(
                model="qwen-mt-flash",
                messages=[
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ],
                temperature=0.2
            )
        )

        result_text = (
            resp
            .choices[0]
            .message.content
        )

        # -------------------
        # JSON解析
        # -------------------

        try:

            result = json.loads(
                result_text
            )

        except Exception:

            raise Exception(
                f"Agent返回非法JSON:\n{result_text}"
            )

        changed_files = []

        # -------------------
        # 写回数据库
        # -------------------

        for item in result.get(
            "files",
            []
        ):

            path = item.get(
                "path"
            )

            content = item.get(
                "content"
            )

            if not path:
                continue

            file = (
                db.query(
                    PluginFile
                )
                .filter(
                    PluginFile.project_id
                    == project.id,
                    PluginFile.path
                    == path
                )
                .first()
            )

            # 已存在
            if file:

                file.content = content

            # 新文件
            else:

                file = PluginFile(
                    project_id=project.id,
                    path=path,
                    language="python",
                    content=content
                )

                db.add(file)

            changed_files.append(
                {
                    "path": path
                }
            )

        db.commit()

        return {
            "files": changed_files
        }