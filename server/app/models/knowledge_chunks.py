from app.core.database import Base
from sqlalchemy import Column,Integer,String,Text,ForeignKey,DateTime
from sqlalchemy import JSON

class KnowledgeChunk(Base):

    __tablename__ = "knowledge_chunks"

    id = Column(Integer, primary_key=True)

    knowledge_id = Column(Integer, index=True)

    file_id = Column(Integer, index=True)

    content = Column(Text)

    chunk_index = Column(Integer)

    embedding = Column(JSON)