from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base


class PluginProject(Base):
    __tablename__ = "plugin_projects"

    id = Column(String, primary_key=True)

    user_id = Column(String, nullable=False)

    name = Column(String, nullable=False)

    description = Column(String)

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