from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from crud import *
from orm_models import *


def main():
    # Step 1: Create the database engine
    engine = create_engine(
        "sqlite:///example.db", echo=False
    )  # Replace with your actual database URL
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Step 2: Create the tables
    Base.metadata.create_all(bind=engine)

    # Step 3: Start a session
    db = SessionLocal()

    # Step 4: Add data to the database
    author_data = AuthorCreate(name="John Doe")
    author = create_author(db, author_data)

    book_data_1 = BookCreate(title="Python 101")
    book_data_2 = BookCreate(title="Advanced Python")

    book_1 = create_book(db, book_data_1)
    book_2 = create_book(db, book_data_2)

    # Step 5: Associate books with the author
    add_books_to_author(db, author_id=author.id, book_ids=[book_1.id, book_2.id])
    # print(f"Added books to author {author.name}")

    # Fetch and print books of author with ID 1
    try:
        books: List[Book] = get_books_of_author(db, author_id=author.id)

        # Print the results
        if books:
            print(f"Books for author {author.name}:")
            for book in books:
                print(f"- {book.title}")
        else:
            print(f"No books found for author {author.name}.")
    except ValueError as e:
        print(e)

    # Step 6: Remove one book from the author
    remove_books_from_author(db, author_id=author.id, book_ids=[book_2.id])
    print(f"Removed book {book_2.title} from author {author.name}")

    # Fetch and print books of author with ID 1
    try:
        books: List[Book] = get_books_of_author(db, author_id=author.id)

        # Print the results
        if books:
            print(f"Books for author {author.name}:")
            for book in books:
                print(f"- {book.title}")
        else:
            print(f"No books found for author {author.name}.")
    except ValueError as e:
        print(e)

    # Step 7: Delete the author and book
    # delete_author(db, author_id=author.id)
    delete_book(db, book_id=book_1.id)

    print("Deleted the author and the book.")

    # Step 8: Close the session
    db.close()


if __name__ == "__main__":
    main()
