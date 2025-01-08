import ulid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship, backref
from backend.database import Base


def generate_ulid():
    """Generate a ULID as the default value for the ID."""
    return str(ulid.new())


class NodeDataORM(Base):
    __tablename__ = "reference_data"

    id = Column(String, primary_key=True, default=generate_ulid, index=True)
    name = Column(String, nullable=False)
    parent_id = Column(String, ForeignKey("reference_data.id"), nullable=True)  # Remove ondelete cascade
    is_folder = Column(Boolean, default=False)
    file_path = Column(String, nullable=True)  # Actual file path on disk
    description = Column(String, nullable=True)

    # Establish self-referential relationship for hierarchy
    children = relationship(
        "NodeDataORM",
        cascade="all, delete-orphan",
        backref=backref("parent", remote_side=[id])
    )
