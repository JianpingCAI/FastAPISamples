from .database import SessionLocal, Base, engine
from .crud import add_email_to_user, create_user, get_user_by_id, get_user_by_name
from .schemas import EmailCreate, UserCreate


def main():
    # Create tables
    Base.metadata.create_all(bind=engine)

    # Creating a new database session
    db = SessionLocal()

    # Creating a new user
    user_data = UserCreate(name="Alice", age=30)
    user = create_user(db=db, user=user_data)
    print(f"Created new user: {user.name}, ID: {user.id}")

    # Fetching a user by name
    user_fetched = get_user_by_name(db=db, name="Alice")
    if user_fetched:
        print(f"Fetched user: {user_fetched.name}, Age: {user_fetched.age}")

    # Adding an email to the user
    email_data1 = EmailCreate(email_address="alice1@example.com")
    email_data2 = EmailCreate(email_address="alice2@example.com")

    email = add_email_to_user(db=db, user_id=user.id, email=email_data1.email_address)
    print(f"Added email: {email.email_address} to user ID: {email.user_id}")

    email = add_email_to_user(db=db, user_id=user.id, email=email_data2.email_address)
    print(f"Added email: {email.email_address} to user ID: {email.user_id}")

    # Fetching and printing all emails associated with the user
    user_updated = get_user_by_id(db=db, id=user.id)
    print(f"User {user_updated.name}'s emails:")
    for email in user_updated.emails:
        print(email.email_address)

    # Close the session
    db.close()


if __name__ == "__main__":
    main()
