# app/services/memory_manager.py
from typing import List
from app.models.memory import Memory
from app.core.database import SessionLocal
from app.models.user import User

import numpy as np

import json

from app.services.embedding_service import (
    get_embedding
)

class MemoryManager:
    SHORT_TERM_LIMIT = 20  # 最近20条为短期记忆

    def __init__(self):
        self.db = SessionLocal()

    def get_recent(self, user_id: int, agent_id: int) -> List[dict]:
        """获取最近N条消息"""
        messages = (
            self.db.query(Memory)
            .filter(Memory.user_id == user_id, Memory.agent_id == agent_id)
            .order_by(Memory.created_at.desc())
            .limit(self.SHORT_TERM_LIMIT)
            .all()
        )
        # 倒序返回，使最新消息在最后
        return [{"role": m.role, "content": m.content} for m in reversed(messages)]

    def search_relevant_memories(
        self,
        user_id: int,
        agent_id: int,
        query: str,
        top_k: int = 5
    ):
        """
        语义检索相关记忆
        """

        # 用户问题 embedding
        query_embedding = get_embedding(query)

        # 查询所有记忆
        memories = (
            self.db.query(Memory)
            .filter(
                Memory.user_id == user_id,
                Memory.agent_id == agent_id
            )
            .all()
        )

        scored_memories = []

        for memory in memories:

            if not memory.embedding:
                continue

            memory_embedding = json.loads(memory.embedding)

            similarity = self.cosine_similarity(
                query_embedding,
                memory_embedding
            )

            scored_memories.append({
                "role": memory.role,
                "content": memory.content,
                "score": similarity
            })

        # 按相似度排序
        scored_memories.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return scored_memories[:top_k]

    def cosine_similarity(self, vec1, vec2):

        vec1 = np.array(vec1)
        vec2 = np.array(vec2)

        return np.dot(vec1, vec2) / (
            np.linalg.norm(vec1)
            * np.linalg.norm(vec2)
        )

    def add_message(
        self,
        user_id: int,
        agent_id: int,
        role: str,
        content: str
    ):

        embedding = get_embedding(content)

        msg = Memory(
            user_id=user_id,
            agent_id=agent_id,
            role=role,
            content=content,
            embedding=json.dumps(embedding)
        )

        self.db.add(msg)

        self.db.commit()

    def get_summary(self, user_id: int, agent_id: int) -> str:
        """长期记忆摘要占位，后续可用embedding或AI生成"""
        # 暂时直接返回空字符串
        return ""
    
    def get_chat_history(
    self,
    user_email: str,
    agent_id: int
    ):

        user = self.db.query(
            User
        ).filter(
            User.email == user_email
        ).first()

        if not user:

            return []

        messages = (

            self.db.query(Memory)

            .filter(
                Memory.user_id == user.id,
                Memory.agent_id == agent_id
            )

            .order_by(
                Memory.created_at.asc()
            )

            .all()

        )

        return [

            {
                "role": m.role,
                "content": m.content
            }

            for m in messages

        ]