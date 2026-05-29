from sqlalchemy import Column,Integer,String,Text,ForeignKey,DateTime

from datetime import datetime

from app.core.database import Base


class Memory(Base):

    __tablename__ = "memories"

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

    # 消息角色
    role = Column(
        String,
        nullable=False
    )

    # 消息内容
    content = Column(
        Text,
        nullable=False
    )

    # 向量Embedding
    embedding = Column(
        Text,
        nullable=True
    )

    # 创建时间
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

