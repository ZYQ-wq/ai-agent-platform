from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class PluginFile(Base):
    __tablename__ = "plugin_files"

    id = Column(String, primary_key=True)

    project_id = Column(
        String,
        ForeignKey("plugin_projects.id")
    )

    path = Column(String)

    language = Column(String)

    content = Column(Text)

    project = relationship(
        "PluginProject",
        back_populates="files"
    )