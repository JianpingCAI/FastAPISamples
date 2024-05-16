from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLAlchemy base class
Base = declarative_base()

# Database connection URL
# DATABASE_URL = "postgresql://postgres:password@localhost/tutorial"
DATABASE_URL = "postgresql://postgres:cai@localhost/tutorial"

# Create an engine instance
engine = create_engine(DATABASE_URL, echo=False)

# Create a sessionmaker bound to the engine
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Base.metadata.create_all(bind=engine)
