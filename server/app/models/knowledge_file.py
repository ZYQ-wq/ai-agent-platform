from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.core.database import Base

class KnowledgeFile(Base):
    __tablename__ = "knowledge_files"

    id = Column(Integer, primary_key=True)

    knowledge_id = Column(Integer, index=True)  # 绑定知识库

    file_name = Column(String(255))

    file_path = Column(String(500))

    file_type = Column(String(50))

    created_at = Column(DateTime, default=datetime.utcnow)