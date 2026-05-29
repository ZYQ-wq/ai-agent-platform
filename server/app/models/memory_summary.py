from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Text,
    DateTime
)

from datetime import datetime

from app.core.database import Base


class MemorySummary(Base):

    __tablename__ = "memory_summaries"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # 所属用户
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    # 所属Agent
    agent_id = Column(
        Integer,
        ForeignKey("agents.id"),
        nullable=False
    )

    # 长期记忆摘要
    summary = Column(
        Text,
        nullable=False,
        default=""
    )

    # 更新时间
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )