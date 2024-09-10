from sqlalchemy import Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Association Table
author_book = Table(
    "author_book",
    Base.metadata,
    Column("author_id", ForeignKey("authors.id"), primary_key=True),
    Column("book_id", ForeignKey("books.id"), primary_key=True),
)


class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    # Many-to-many relationship with Book
    books = relationship("Book", secondary=author_book, back_populates="authors")


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    # Many-to-many relationship with Author
    authors = relationship("Author", secondary=author_book, back_populates="books")
