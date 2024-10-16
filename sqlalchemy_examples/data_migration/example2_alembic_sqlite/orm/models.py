from sqlalchemy import (
    Sequence,
    create_engine,
    Column,
    Integer,
    String,
    ForeignKey,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Declare the base
Base = declarative_base()


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(Text, nullable=True)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    item_name = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="orders")


Customer.orders = relationship("Order", order_by=Order.id, back_populates="customer")

# Set up the database engine
engine = create_engine("sqlite:///./test_sqlite.db", echo=True)


# Create all tables in the database
def create_database():
    Base.metadata.create_all(engine)


# Base.metadata.create_all(engine)

# print("********************Tables created successfully.")
