import numpy as np

from app.core.database import SessionLocal
from app.models.knowledge_chunks import KnowledgeChunk

from app.services.embedding_service import get_embedding

def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a)
        * np.linalg.norm(b)
    )


def search_kb_service(
    kb_id: int,
    query: str,
    top_k: int = 5
):

    db = SessionLocal()

    try:

        query_vector = get_embedding(query)

        chunks = db.query(
            KnowledgeChunk
        ).filter(
            KnowledgeChunk.knowledge_id == kb_id
        ).all()

        scores = []

        for chunk in chunks:

            if not chunk.embedding:
                continue

            score = cosine_similarity(
                query_vector,
                chunk.embedding
            )

            scores.append({
                "content": chunk.content,
                "score": float(score)
            })

        scores.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return scores[:top_k]

    finally:
        db.close()