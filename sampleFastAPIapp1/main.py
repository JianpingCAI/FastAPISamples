from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Integer, String, Table, Column, ForeignKey, Sequence

# Database setup
# DATABASE_URL = "duckdb:///:memory:"
DATABASE_URL = "duckdb:///./test.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Association Table
author_book = Table(
    "author_book",
    Base.metadata,
    Column("author_id", Integer, ForeignKey("author.id"), primary_key=True),
    Column("book_id", Integer, ForeignKey("book.id"), primary_key=True),
)

author_id_seq = Sequence("author_id_seq")


class Author(Base):
    __tablename__ = "author"
    id = Column(
        Integer,
        author_id_seq,
        server_default=author_id_seq.next_value(),
        primary_key=True,
    )
    name = Column(String)
    books = relationship("Book", secondary=author_book, back_populates="authors")


book_id_seq = Sequence("book_id_seq")


class Book(Base):
    __tablename__ = "book"
    id = Column(
        Integer, book_id_seq, server_default=book_id_seq.next_value(), primary_key=True
    )
    title = Column(String)
    authors = relationship("Author", secondary=author_book, back_populates="books")


# Create the database tables
Base.metadata.create_all(bind=engine)

# FastAPI app
app = FastAPI()


# Dependency to get the DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/authors/")
async def create_author(name: str, db: Session = Depends(get_db)):
    author = Author(name=name)
    db.add(author)
    db.commit()
    db.refresh(author)
    return author


@app.get("/authors/")
async def read_authors(db: Session = Depends(get_db)):
    authors = db.query(Author).all()
    return authors


@app.post("/books/")
async def create_book(title: str, db: Session = Depends(get_db)):
    book = Book(title=title)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@app.get("/books/")
async def read_books(db: Session = Depends(get_db)):
    books = db.query(Book).all()
    return books


@app.post("/authors/{author_id}/add_book/")
async def add_book_to_author(author_id: int, title: str, db: Session = Depends(get_db)):
    # Fetch the author by ID
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if the book already exists, otherwise create a new one
    book = db.query(Book).filter(Book.title == title).first()
    if not book:
        book = Book(title=title)
        db.add(book)
        db.commit()
        db.refresh(book)

    # Add the book to the author's collection
    author.books.append(book)
    db.commit()

    return {
        "message": "Book added to author",
        "author_id": author.id,
        "book_id": book.id,
    }


# Run the application
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
