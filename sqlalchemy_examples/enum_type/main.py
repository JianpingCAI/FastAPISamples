from sqlalchemy import create_engine, Column, Integer, String, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, sessionmaker
from pydantic import BaseModel
import enum


# Enum for SQLAlchemy
class PostStatus(enum.Enum):
    draft = "draft"
    published = "published"
    archived = "archived"


# SQLAlchemy Base and engine setup
Base = declarative_base()
engine = create_engine("sqlite:///:memory:")
Session = sessionmaker(bind=engine)


# SQLAlchemy Model
class BlogPost(Base):
    __tablename__ = "blog_posts"
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    status = Column(Enum(PostStatus))


# Create database tables
Base.metadata.create_all(engine)


# Pydantic Model for validation
class BlogPostSchema(BaseModel):
    title: str
    status: PostStatus


# Example Usage
def main():
    # Creating a new session
    session = Session()

    # Example data, ideally coming from an API endpoint or user input
    post_data = {"title": "Introduction to SQLAlchemy", "status": "draft"}

    # Validating data using Pydantic
    valid_post = BlogPostSchema(**post_data)

    # Creating a new BlogPost instance from validated data
    new_post = BlogPost(title=valid_post.title, status=valid_post.status)

    # Adding and committing the new post to the database
    session.add(new_post)
    session.commit()

    # Querying the database to show the inserted data
    inserted_post = session.query(BlogPost).first()
    print(
        f"Inserted Post: Title - {inserted_post.title}, Status - {inserted_post.status}"
    )


if __name__ == "__main__":
    main()
