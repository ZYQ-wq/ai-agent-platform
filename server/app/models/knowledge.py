from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base


class Knowledge(Base):
    __tablename__ = "knowledge_bases"

    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, index=True)

    name = Column(String(255))          # 知识库名称

    description = Column(String(1000))  # 简介（你缺的）

    created_at = Column(DateTime, default=datetime.utcnow)