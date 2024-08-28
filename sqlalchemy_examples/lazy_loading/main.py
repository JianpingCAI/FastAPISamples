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

    environments = relationship("Environment", back_populates="script")


# Environment class for one-to-many/many-to-one relationship
class Environment(Base):
    __tablename__ = "environment"
    id = Column(Integer, primary_key=True)
    script_id = Column(Integer, ForeignKey("script.id"))

    script = relationship("Script", back_populates="environments")


# Step 3: Creating the Database
Base.metadata.create_all(engine)

# Step 4: Adding Test Data

session = Session()

#############################
# Adding Script and Children
script1 = Script()
environment1 = Environment(script=script1)
environment2 = Environment(script=script1)
session.add_all([script1, environment1, environment2])

session.commit()

# Step 5: Querying and Displaying Results

# Query for Script-Environment relationship

# Lazy loading
# scripts = session.query(Script).all()

# Eager loading
scripts = session.query(Script).options(joinedload(Script.environments)).all()

# Eager loading 2
# scripts = session.query(Script).options(subqueryload(Script.environments)).all()


print("Scripts:")

for script in scripts:
    print(f"Script ID: {script.id}, Number of environment: {len(script.environments)}")


print("Done!")
