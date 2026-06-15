from app.core.database import Base
from sqlalchemy import Column,Integer,String,Text,ForeignKey,DateTime


class KnowledgeChunk(Base):

    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True)

    knowledge_id = Column(Integer, index=True)

    file_id = Column(Integer, index=True)  # ⚠️ 关键补充（建议加）

    content = Column(Text)

    chunk_index = Column(Integer)