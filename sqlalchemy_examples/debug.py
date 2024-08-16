from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Table,
    Sequence,
)
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base

# Step 1: Database Setup
# engine = create_engine('sqlite:///:memory:', echo=True)
# engine = create_engine("sqlite:///./relationships.db", echo=True)
engine = create_engine("duckdb:///./relationships.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


#############################################################################
# Parent class for one-to-many/many-to-one relationship
id_seq3 = Sequence("id_seq3")


class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, id_seq3, server_default=id_seq3.next_value(), primary_key=True)
    children = relationship("Child", back_populates="parent")


# Child class for one-to-many/many-to-one relationship
id_seq4 = Sequence("id_seq4")


class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, id_seq4, server_default=id_seq4.next_value(), primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))
    parent = relationship("Parent", back_populates="children")


# Step 3: Creating the Database
Base.metadata.create_all(engine)


#############################
# Adding Parent and Children
parent1 = Parent()
child1 = Child(parent=parent1)
child2 = Child(parent=parent1)
session.add_all([parent1, child1, child2])


session.commit()


session.close()
