from openai import OpenAI
from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL
)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL,
)


def call_qwen(prompt: str) -> str:

    messages = [
        {"role": "user", "content": prompt}
    ]

    resp = client.chat.completions.create(
        model="qwen-max",
        messages=messages
    )

    return resp.choices[0].message.content