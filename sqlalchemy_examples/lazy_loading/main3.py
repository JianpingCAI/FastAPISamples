from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker, joinedload, subqueryload
from sqlalchemy.orm import declarative_base
from typing import List, Tuple

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
    application_id = Column(Integer, ForeignKey("application.id"))

    application = relationship("Application", back_populates="environments")


class Application(Base):
    __tablename__ = "application"
    id = Column(Integer, primary_key=True)
    name = Column(String(50))

    environments = relationship("Environment", back_populates="application")


# Step 3: Creating the Database
Base.metadata.create_all(engine)

# Step 4: Adding Test Data

session = Session()

application = Application(name="app")
session.add(application)
session.commit()
session.refresh(application)

script1 = Script()
session.add(script1)
session.commit()

session.refresh(script1)

environment1 = Environment(script_id=script1.id, application=application)
environment2 = Environment(script_id=script1.id, application=application)
session.add_all([environment1, environment2])
session.commit()

# Step 5: Querying Environment and Script Together
print("*********Environment and Script Together:")

# Join Environment with Script based on script_id
# Join Environment with Script and Application based on script_id and application_id
results: List[Tuple[Environment, Script, Application]] = (
    session.query(Environment, Script, Application)
    .join(Script, Environment.script_id == Script.id)
    .join(Application, Environment.application_id == Application.id)
    .all()
)

print("********* Display:")

# Displaying the results
for environment, script, application in results:
    print(
        f"Environment ID: {environment.id}, Associated Script ID: {script.id}, Application: {application.name}"
    )


print("Done!")
