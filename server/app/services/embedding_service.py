import json
from typing import Any

from openai import OpenAI

from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL
)

EMBEDDING_MODEL = "text-embedding-v1"

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


def normalize_embedding_vector(
    value: Any
) -> list[float]:
    if value is None:
        return []

    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError:
            return []

    if not isinstance(value, (list, tuple)):
        return []

    vector = []
    for item in value:
        try:
            vector.append(float(item))
        except (TypeError, ValueError):
            return []

    return vector


def get_embedding(text: str) -> list[float]:
    if not (text or "").strip():
        raise ValueError("Embedding 输入文本不能为空")

    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text
    )

    vector = normalize_embedding_vector(
        response.data[0].embedding
    )

    if not vector:
        raise ValueError("Embedding 返回为空")

    return vector
