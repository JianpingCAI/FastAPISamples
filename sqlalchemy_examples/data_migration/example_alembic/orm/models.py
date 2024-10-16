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

custom_id_seq = Sequence("custom_id_seq")
order_id_seq = Sequence("order_id_seq")


class Customer(Base):
    __tablename__ = "customers"

    # id = Column(Integer, primary_key=True)
    id = Column(
        Integer,
        custom_id_seq,
        server_default=custom_id_seq.next_value(),
        primary_key=True,
    )
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    # id = Column(Integer, primary_key=True)
    id = Column(
        Integer,
        order_id_seq,
        server_default=order_id_seq.next_value(),
        primary_key=True,
    )
    item_name = Column(String, nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    customer = relationship("Customer", back_populates="orders")


Customer.orders = relationship("Order", order_by=Order.id, back_populates="customer")

# Set up the database engine
engine = create_engine("duckdb:///test_duckdb.db", echo=False)

# Create all tables in the database
Base.metadata.create_all(engine)
