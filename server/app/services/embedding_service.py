from openai import OpenAI

from app.core.config import (
    OPENAI_API_KEY,
    OPENAI_BASE_URL
)

client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url=OPENAI_BASE_URL
)


def get_embedding(text: str):

    response = client.embeddings.create(
        model="text-embedding-v1",
        input=text
    )

    return response.data[0].embedding