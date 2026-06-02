# app/models/tool_call.py
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.core.database import Base

class ToolCall(Base):
    __tablename__ = "tool_calls"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    tool_name = Column(String, nullable=False)
    arguments = Column(Text, nullable=True)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)