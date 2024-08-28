from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.orm.base import Base

DATABASE_URL = "sqlite:///./blog_platform.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
