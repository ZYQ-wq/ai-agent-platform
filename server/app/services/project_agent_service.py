
from sqlalchemy.orm import Session

from openai import OpenAI

from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL
)

from app.models.agent import Agent
from app.models.plugin_project import PluginProject
from app.models.plugin_file import PluginFile

import re

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

DEFAULT_CODING_AGENT_PROMPT = """
你是一名全栈软件工程师，擅长编写完整、可运行的小型应用。
生成 Web 应用时优先使用 index.html + CSS + JavaScript 单页或多文件结构。
每次输出必须是完整文件内容，禁止省略、禁止占位符、禁止 "// existing code"。
"""


class ProjectAgentService:

    @staticmethod
    def strip_code_fences(content: str) -> str:
        content = (content or "").strip()

        fenced = re.match(
            r"^```(?:[a-zA-Z0-9_-]+)?\s*\r?\n([\s\S]*?)\r?\n```\s*$",
            content
        )
        if fenced:
            return fenced.group(1).strip()

        content = re.sub(
            r"^```(?:[a-zA-Z0-9_-]+)?\s*\r?\n?",
            "",
            content
        )
        content = re.sub(
            r"\r?\n?```\s*$",
            "",
            content
        )

        return content.strip()

    @staticmethod
    def parse_file_blocks(
        text: str
    ):

        files = []

        pattern = re.compile(
            r"FILE:\s*(.+?)\s*\r?\n"
            r"ACTION:\s*(.+?)\s*\r?\n"
            r"([\s\S]*?)"
            r"(?=\r?\nFILE:|\Z)",
            re.IGNORECASE
        )

        matches = pattern.findall(
            text or ""
        )

        for path, action, content in matches:
            cleaned = ProjectAgentService.strip_code_fences(
                content
            )

            files.append(
                {
                    "path": path.strip(),
                    "action": action.strip().lower(),
                    "content": cleaned
                }
            )

        return files

    @staticmethod
    def run_agent(
        db: Session,
        project_id: str,
        prompt: str
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

        agent_prompt = DEFAULT_CODING_AGENT_PROMPT

        if project.agent_id:
            agent = (
                db.query(
                    Agent
                )
                .filter(
                    Agent.id == project.agent_id
                )
                .first()
            )

            if agent and agent.system_prompt:
                agent_prompt = agent.system_prompt

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

        project_context = ""

        for file in files:
            content = (
                file.content or ""
            )[:8000]

            project_context += f"""
FILE:
{file.path}

CONTENT:
{content}

================================

"""

        final_prompt = f"""
你是一个高级软件开发 Agent。

Agent 配置：

{agent_prompt}

当前项目文件：

{project_context}

用户需求：

{prompt}

请根据需求生成完整、可运行的代码。

规则：
1. 只输出 FILE / ACTION / 代码，不要 JSON，不要解释。
2. 每个文件必须输出完整内容，禁止省略。
3. Web 小应用优先创建或修改 index.html、style.css、script.js 等文件。
4. 如果默认模板文件 main.py / plugin.yaml / README.md 不需要，可以 ACTION: delete。
5. 如果文件已存在且需要更新，使用 ACTION: modify 并给出完整新内容。
6. 如果文件不存在，使用 ACTION: create。

格式示例：

FILE: index.html
ACTION: create
```html
<!DOCTYPE html>
<html>...</html>
```

FILE: style.css
ACTION: create
```css
body {{ margin: 0; }}
```

开始输出。
"""

        resp = (
            client.chat.completions.create(
                model="qwen-max",
                messages=[
                    {
                        "role": "user",
                        "content": final_prompt
                    }
                ],
                temperature=0.2,
                timeout=120.0
            )
        )

        result_text = (
            resp
            .choices[0]
            .message.content
            or ""
        )

        parsed_files = (
            ProjectAgentService
            .parse_file_blocks(
                result_text
            )
        )

        valid_files = [
            item
            for item in parsed_files
            if item["content"].strip()
            or item["action"] == "delete"
        ]

        if not valid_files:
            return {
                "message":
                    "未能解析到有效代码，请重试。"
                    "请确保需求描述清晰，例如："
                    "生成一个可运行的井字棋网页应用。",
                "files": []
            }

        skipped = len(parsed_files) - len(valid_files)

        message = (
            f"发现 {len(valid_files)} 个有效文件变更"
        )

        if skipped > 0:
            message += (
                f"，已忽略 {skipped} 个空内容文件"
            )

        return {
            "message": message,
            "files": valid_files
        }
