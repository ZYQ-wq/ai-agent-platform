from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.core.database import Base


class WorkflowEdge(Base):

    __tablename__ = "workflow_edges"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    workflow_id = Column(
        Integer,
        ForeignKey("workflows.id"),
        nullable=False
    )

    source_node = Column(
        String(100),
        nullable=False
    )

    target_node = Column(
        String(100),
        nullable=False
    )