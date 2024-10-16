from orm.models import sessionmaker, engine, Customer, Order

# Create a sessionmaker bound to the engine
Session = sessionmaker(bind=engine)

# Create a session
session = Session()

# Example usage
# new_customer = Customer(name="John Doe")
# session.add(new_customer)
# session.commit()


# Querying data
customers = session.query(Customer).all()
for customer in customers:
    # customer.orders.append(Order(item_name="Item 1", customer_id=customer.id))
    print(customer.id, customer.name, customer.email)

# session.commit()

print("-------------Orders-------------")
orders = session.query(Order).all()
for order in orders:
    print(order.id, order.item_name, order.customer_id)