# initialize_db.py
from models.database import Base, engine
from models.task import Task

Base.metadata.create_all(bind=engine)
