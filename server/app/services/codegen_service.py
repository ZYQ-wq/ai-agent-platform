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