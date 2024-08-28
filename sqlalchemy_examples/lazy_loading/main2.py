from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, joinedload, subqueryload
from sqlalchemy.orm import declarative_base

# Step 1: Database Setup
engine = create_engine("sqlite:///:memory:", echo=True)
# engine = create_engine("sqlite:///./relationships.db", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()


#############################################################################
# Script class for one-to-many/many-to-one relationship
class Script(Base):
    __tablename__ = "script"
    id = Column(Integer, primary_key=True)


# Environment class for one-to-many/many-to-one relationship
class Environment(Base):
    __tablename__ = "environment"
    id = Column(Integer, primary_key=True)
    script_id = Column(Integer, ForeignKey("script.id"))


# Step 3: Creating the Database
Base.metadata.create_all(engine)

# Step 4: Adding Test Data

session = Session()

#############################
# Adding Script and Children
script1 = Script()
# environment1 = Environment(script=script1)
# environment2 = Environment(script=script1)
# session.add_all([script1, environment1, environment2])
session.add(script1)

session.commit()

session.refresh(script1)

environment1 = Environment(script_id=script1.id)
environment2 = Environment(script_id=script1.id)
session.add_all([environment1, environment2])
session.commit()

# Step 5: Querying and Displaying Results
print("*********Scripts:")

# Query for Script-Environment relationship
scripts = session.query(Script).all()


print("*********Scripts:")

for script in scripts:
    # Manually query environments related to this script
    environments = (
        session.query(Environment).filter(Environment.script_id == script.id).all()
    )
    print(f"Script ID: {script.id}, Number of environments: {len(environments)}")


print("Done!")
