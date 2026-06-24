
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
你是一个高级软件开发 Agent。

Agent 配置：

{agent.system_prompt}

{project_context}

{prompt}

请分析当前项目。

决定：

哪些文件需要创建
哪些文件需要修改
哪些文件需要删除

不要直接执行修改。

不要解释。

不要返回 JSON。

创建文件：
例如：
FILE: index.html
ACTION: create

```html
<html>
 ···
<html>

修改文件：

FILE: main.py
ACTION: modify

完整文件内容

删除文件：

FILE: old.py
ACTION: delete

一个文件对应一个 FILE 块
content 必须是完整文件

不要输出：

// existing code

// omitted

原有代码省略

等内容

必须返回完整代码
如果没有变化，不要返回该文件
可以返回多个 FILE 块

例如：

FILE: index.html
ACTION: create

...

FILE: style.css
ACTION: create

...

FILE: app.py
ACTION: modify

...
不允许返回 JSON
不允许解释
只输出 FILE + ACTION + 代码块

开始分析。
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

        parsed_files = (
            ProjectAgentService
            .parse_file_blocks(
                result_text
            )
        )

        print("====== Parsed Files ======")

        for f in parsed_files:
            print(
                f["action"],
                f["path"]
            )

        print("====== Agent Prompt ======")
        print(agent.system_prompt)

        print("====== Final Prompt ======")
        print(final_prompt) 

        return {
            "message":
                f"发现 {len(parsed_files)} 个文件变更",

            "files":
                parsed_files
        }
    
    @staticmethod
    def parse_file_blocks(
        text: str
    ):

        files = []

        pattern = re.compile(
            r"FILE:\s*(.+?)\s*\nACTION:\s*(.+?)\s*\n([\s\S]*?)(?=\nFILE:|\Z)",
            re.S
        )

        matches = pattern.findall(
            text
        )

        for path, action, content in matches:

            # 去掉 markdown 代码块
            content = re.sub(
                r"^```[a-zA-Z0-9]*\n?",
                "",
                content.strip()
            )

            content = re.sub(
                r"\n```$",
                "",
                content.strip()
            )

            files.append(
                {
                    "path": path.strip(),
                    "action": action.strip(),
                    "content": content.strip()
                }
            )

        return files