import ulid
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

# SQLAlchemy base class
Base = declarative_base()


# Helper function to generate ULIDs as strings
def generate_ulid():
    return str(ulid.new())


# Self-referential model using ULIDs
class FileSystem(Base):
    __tablename__ = "file_system"

    # Use String for the primary key, with default=generate_ulid
    id = Column(String, primary_key=True, default=generate_ulid)
    name = Column(String, nullable=False)

    # Parent ID is also a string, referencing file_system.id
    parent_id = Column(String, ForeignKey("file_system.id"), nullable=True)  # Removed ondelete cascade

    # Relationships
    parent = relationship("FileSystem", remote_side=[id], back_populates="children")
    children = relationship("FileSystem", back_populates="parent", cascade="all, delete-orphan")

    def __repr__(self):
        return f"FileSystem(id={self.id}, name='{self.name}', parent_id={self.parent_id})"


# Create an in-memory DuckDB engine
engine = create_engine("duckdb:///:memory:")
# # Create an in-memory SQLite engine
# engine = create_engine("sqlite:///:memory:")

# Create tables
Base.metadata.create_all(engine)


# Populate the file system hierarchy
def populate_file_system():
    with Session(engine) as session:
        root = FileSystem(name="root")  # ULID auto-generated
        folder1 = FileSystem(name="folder1", parent=root)  # ULID auto-generated
        folder2 = FileSystem(name="folder2", parent=root)  # ULID auto-generated
        file1 = FileSystem(name="file1", parent=folder1)  # ULID auto-generated
        file2 = FileSystem(name="file2", parent=folder2)  # ULID auto-generated

        # Add everything to the session and commit
        session.add(root)
        session.commit()


# Simplified deletion function
def delete_folder_with_cascade(folder_id):
    with Session(engine) as session:
        folder = session.get(FileSystem, folder_id)
        if not folder:
            print(f"No folder found with id={folder_id}")
            return

        def delete_recursively(item):
            # Delete children first (bottom-up)
            for child in item.children[:]:  # Use slice copy to avoid modification during iteration
                delete_recursively(child)
            print(f"Deleting: {item}")
            session.delete(item)
            session.commit()  # Commit the session after each delete # !!! important
            # however, committng the session after each delete breaks the transactional feature of the operation.

        delete_recursively(folder)
        session.commit()


# Utility function to display all items
def show_all_items(header="Items in FileSystem"):
    with Session(engine) as session:
        items = session.query(FileSystem).all()
        print(f"\n{header}:")
        for item in items:
            print(item)


# Run a small demo
if __name__ == "__main__":
    # Insert sample data
    populate_file_system()

    # Show all items before deletion
    show_all_items("Before Deletion")

    # Retrieve folder1's ULID
    with Session(engine) as session:
        folder1 = session.query(FileSystem).filter_by(name="folder1").first()

    # Delete folder1 (and its children) by ULID
    if folder1:
        print(f"\nDeleting folder1 by ULID={folder1.id}:")
        delete_folder_with_cascade(folder1.id)

    # Show all items after deletion
    show_all_items("After Deletion")
