import numpy as np

from app.core.database import SessionLocal
from app.models.knowledge_chunks import KnowledgeChunk

from app.services.embedding_service import (
    get_embedding,
    normalize_embedding_vector,
    EMBEDDING_MODEL,
)


class EmbeddingDimensionError(Exception):
    def __init__(
        self,
        query_dim: int,
        stored_dim: int,
        mismatched_count: int,
        total_count: int
    ):
        self.query_dim = query_dim
        self.stored_dim = stored_dim
        self.mismatched_count = mismatched_count
        self.total_count = total_count
        super().__init__(
            f"向量维度不一致：检索向量 {query_dim} 维（{EMBEDDING_MODEL}），"
            f"知识库中有 {mismatched_count}/{total_count} 条切片为 "
            f"{stored_dim} 维旧索引。请删除并重新上传文档以重建向量。"
        )


def cosine_similarity(a, b) -> float:
    a = np.array(a, dtype=float)
    b = np.array(b, dtype=float)

    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a == 0 or norm_b == 0:
        return 0.0

    return float(np.dot(a, b) / (norm_a * norm_b))


def search_kb_service(
    kb_id: int,
    query: str,
    top_k: int = 5
):
    db = SessionLocal()

    try:
        query_vector = get_embedding(query)
        query_dim = len(query_vector)

        chunks = db.query(
            KnowledgeChunk
        ).filter(
            KnowledgeChunk.knowledge_id == kb_id
        ).all()

        if not chunks:
            return []

        scores = []
        skipped_empty = 0
        mismatched_dim = None
        mismatched_count = 0
        valid_count = 0

        for chunk in chunks:
            chunk_vector = normalize_embedding_vector(
                chunk.embedding
            )

            if not chunk_vector:
                skipped_empty += 1
                continue

            valid_count += 1

            if len(chunk_vector) != query_dim:
                mismatched_dim = len(chunk_vector)
                mismatched_count += 1
                continue

            score = cosine_similarity(
                query_vector,
                chunk_vector
            )

            scores.append({
                "content": chunk.content,
                "score": score
            })

        if scores:
            scores.sort(
                key=lambda x: x["score"],
                reverse=True
            )
            return scores[:top_k]

        if mismatched_count > 0 and mismatched_dim is not None:
            raise EmbeddingDimensionError(
                query_dim=query_dim,
                stored_dim=mismatched_dim,
                mismatched_count=mismatched_count,
                total_count=valid_count
            )

        if skipped_empty == len(chunks):
            raise ValueError(
                "知识库切片缺少有效向量，请重新上传文档。"
            )

        return []

    finally:
        db.close()
