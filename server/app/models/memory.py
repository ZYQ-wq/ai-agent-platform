from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.core.database import Base

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String) # user 或 assistant
    content = Column(Text)