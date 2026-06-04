from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import ForeignKey

from app.core.database import Base


class WorkflowNode(Base):

    __tablename__ = "workflow_nodes"

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

    node_id = Column(
        String(100),
        nullable=False
    )

    node_type = Column(
        String(50),
        nullable=False
    )

    name = Column(
        String(255),
        nullable=False
    )

    inputs = Column(Text)

    outputs = Column(Text)

    config = Column(
        Text,
        nullable=True
    )