from sqlalchemy.orm import Session
from orm_models import *
from data_models import *
from typing import List


# Add a new author
def create_author(db: Session, author_data: AuthorCreate):
    new_author = Author(name=author_data.name)
    db.add(new_author)
    db.commit()
    db.refresh(new_author)
    return new_author


# Add a new book
def create_book(db: Session, book_data: BookCreate):
    new_book = Book(title=book_data.title)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


# Associate books with an author
def add_books_to_author(db: Session, author_id: int, book_ids: List[int]):
    # Fetch the author by id
    author = db.query(Author).filter(Author.id == author_id).first()
    if not author:
        raise ValueError(f"Author with id {author_id} not found")
    
    # Fetch the books to associate
    books_to_add = db.query(Book).filter(Book.id.in_(book_ids)).all()
    
    # Check if the books to add exist
    if not books_to_add:
        raise ValueError(f"No books found with the provided book_ids: {book_ids}")
    
    # Add books to the author
    for book in books_to_add:
        if book not in author.books:
            author.books.append(book)  # Avoid duplicate additions
    
    # Commit the changes to persist the relationship
    db.commit()

    return author


# def add_books_to_author(db: Session, author_id: int, book_ids: List[int]):
#     author = db.query(Author).filter(Author.id == author_id).first()
#     if not author:
#         raise ValueError(f"Author with id {author_id} not found")

#     # Fetch books to associate
#     books_to_add = db.query(Book).filter(Book.id.in_(book_ids)).all()
#     author.books.extend(books_to_add)

#     db.commit()
#     return author


# Remove specific books from an author
def remove_books_from_author(db: Session, author_id: int, book_ids: List[int]):
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise ValueError(f"Author with id {author_id} not found")

    books_to_remove = db.query(Book).filter(Book.id.in_(book_ids)).all()

    for book in books_to_remove:
        if book in author.books:
            author.books.remove(book)

    db.commit()


# Delete an author by id
def delete_author(db: Session, author_id: int):
    author = db.query(Author).filter(Author.id == author_id).first()

    if author:
        db.delete(author)
        db.commit()
    else:
        raise ValueError(f"Author with id {author_id} not found")


# Delete a book by id
def delete_book(db: Session, book_id: int):
    book = db.query(Book).filter(Book.id == book_id).first()

    if book:
        db.delete(book)
        db.commit()
    else:
        raise ValueError(f"Book with id {book_id} not found")


def get_books_of_author(db: Session, author_id: int) -> List[Book]:
    # Fetch the author by id
    author = db.query(Author).filter(Author.id == author_id).first()

    if not author:
        raise ValueError(f"Author with id {author_id} not found")

    # Fetch the books associated with the author
    books = author.books
    return books
