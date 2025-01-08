import ulid
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

# SQLAlchemy base class
Base = declarative_base()


# Helper function to generate ULIDs as strings
def generate_ulid():
    return str(ulid.new())


class FileSystem(Base):
    __tablename__ = "file_system"

    id = Column(String, primary_key=True, default=generate_ulid)
    name = Column(String, nullable=False)
    # Remove ondelete="CASCADE" to avoid ParserException in DuckDB
    parent_id = Column(String, ForeignKey("file_system.id"), nullable=True)

    # Use cascade="all, delete-orphan" to enforce cascading deletes at the ORM level
    # passive_deletes=True essentially tells SQLAlchemy that the DB *might* handle
    # it, but in DuckDB's case, it's actually the ORM that will do the work.
    parent = relationship("FileSystem", remote_side=[id], back_populates="children")
    children = relationship(
        "FileSystem",
        back_populates="parent",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __repr__(self):
        return f"FileSystem(id={self.id}, name='{self.name}', parent_id={self.parent_id})"


# Create an in-memory DuckDB engine
engine = create_engine("duckdb:///:memory:")

# Create tables
Base.metadata.create_all(engine)


def populate_file_system():
    """Populate the file_system table with some sample data."""
    with Session(engine) as session:
        root = FileSystem(name="root")
        folder1 = FileSystem(name="folder1", parent=root)
        folder2 = FileSystem(name="folder2", parent=root)
        file1 = FileSystem(name="file1", parent=folder1)
        file2 = FileSystem(name="file2", parent=folder2)

        session.add(root)
        session.commit()


def delete_folder_with_cascade(folder_id):
    """Delete a folder (and its children) by ULID, relying on ORM-level cascade."""
    with Session(engine) as session:
        folder = session.get(FileSystem, folder_id)
        if not folder:
            print(f"No folder found with id={folder_id}")
            return

        print(f"Deleting {folder} (children will be cascade-deleted by ORM).")
        session.delete(folder)  # ORM cascade will delete its children
        session.commit()


def show_all_items(header="Items in FileSystem"):
    with Session(engine) as session:
        items = session.query(FileSystem).all()
        print(f"\n{header}:")
        for item in items:
            print(item)


if __name__ == "__main__":
    # Insert sample data
    populate_file_system()

    # Show all items before deletion
    show_all_items("Before Deletion")

    # Retrieve folder1's ULID
    with Session(engine) as session:
        folder1 = session.query(FileSystem).filter_by(name="folder1").first()

    if folder1:
        # Delete folder1 (and its children) via ORM cascading
        delete_folder_with_cascade(folder1.id)

    # Show all items after deletion
    show_all_items("After Deletion")
