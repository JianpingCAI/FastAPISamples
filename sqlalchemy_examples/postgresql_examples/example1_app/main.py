from .database import SessionLocal, Base, engine
from .crud import add_email_to_user, create_user, get_user_by_id, get_user_by_name
from .schemas import EmailCreate, UserCreate
from .models import User as dbUser
import json


def test_JSONB(session):
    # Adding a new hobby to Alice's record
    alice = session.query(dbUser).filter_by(name="Alice").first()
    if alice:
        # Assuming 'hobbies' is a list in JSONB
        alice_hobbies = alice.attributes.get("hobbies", [])
        alice_hobbies.append("swimming")
        alice.attributes["hobbies"] = alice_hobbies
        session.commit()

    # Query for users whose hobbies include 'hiking'
    query = session.query(dbUser).filter(
        dbUser.attributes["hobbies"].contains(["hiking"])
    )
    hikers = query.all()

    print("Users who like hiking:")
    for user in hikers:
        print(f"{user.name}, Hobbies: {user.attributes['hobbies']}")

    # # Set 'verified' status to True for all users who like chess
    # session.query(dbUser).filter(dbUser.attributes["hobbies"].contains(["chess"])).update(
    #     {dbUser.attributes["verified"]: True}, synchronize_session="fetch"
    # )
    # session.commit()


# # Inserting sample users with JSONB data
# users_data = [
#     {"name": "Alice", "age": 28, "attributes": {"hobbies": ["cycling", "hiking"], "verified": True}},
#     {"name": "Bob", "age": 34, "attributes": {"hobbies": ["reading", "chess"], "verified": False}},
#     {"name": "Charlie", "age": 25, "attributes": {"hobbies": ["gaming", "hiking"], "verified": True}}
# ]


def main():
    # Drop all tables (be careful with this in production)
    Base.metadata.drop_all(engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    # Creating a new database session
    db = SessionLocal()

    # Creating a new user
    user_data = UserCreate(
        name="Alice",
        age=30,
        attributes=json.dumps({"hobbies": ["cycling", "hiking"], "verified": True}),
    )
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
    print(f"dbUser {user_updated.name}'s emails:")
    for email in user_updated.emails:
        print(email.email_address)

    test_JSONB(db)

    # Close the session
    db.close()


if __name__ == "__main__":
    main()
