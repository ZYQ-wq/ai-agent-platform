
from sqlalchemy import Column,Integer,String,Text,ForeignKey,DateTime

from datetime import datetime

from app.core.database import Base


class Agent(Base):

    __tablename__ = "agents"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # Agent所属用户
    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    # Agent名称
    name = Column(
        String,
        nullable=False
    )

    # 简介
    description = Column(
        Text,
        nullable=True
    )

    # 系统Prompt
    system_prompt = Column(
        Text,
        nullable=False
    )

    # 创建时间
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

