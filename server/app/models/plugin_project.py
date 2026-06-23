from sqlalchemy import (
    Column,
    String,
    DateTime,
    ForeignKey,
    Integer
)

from sqlalchemy.orm import relationship

from datetime import datetime

from app.core.database import Base


class PluginProject(Base):
    __tablename__ = "plugin_projects"

    id = Column(
        String,
        primary_key=True
    )

    user_id = Column(
        String,
        nullable=False
    )

    name = Column(
        String,
        nullable=False
    )

    description = Column(String)

    # 新增
    agent_id = Column(
        Integer,
        ForeignKey("agents.id"),
        nullable=True
    )

    runtime = Column(
        String,
        default="python"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    files = relationship(
        "PluginFile",
        back_populates="project",
        cascade="all, delete-orphan"
    )