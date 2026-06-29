import os

from openai import OpenAI

from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL
)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)

class CodeGenService:

    @staticmethod
    def generate_code(
        requirement: str
    ):

        prompt = f"""
你是资深Python工程师。

根据需求生成完整代码。

需求：
{requirement}

只返回代码。
不要解释。
"""

        resp = client.chat.completions.create(
            model="qwen-mt-flash",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3
        )

        code = (
            resp.choices[0]
            .message
            .content
        )

        return code
    
    @staticmethod
    def edit_code(
        content: str,
        prompt: str
    ):

        final_prompt = f"""
    你是资深Python工程师。

    请根据要求修改下面代码。

    要求：
    {prompt}

    当前代码：

    {content}

    返回完整修改后的代码。

    只返回代码。
    不要解释。
    不要Markdown。
    不要```python。
    """

        resp = client.chat.completions.create(
            model="qwen-mt-flash",

            messages=[
                {
                    "role": "user",
                    "content": final_prompt
                }
            ],

            temperature=0.2
        )

        code = (
            resp.choices[0]
            .message
            .content
        )

        return code