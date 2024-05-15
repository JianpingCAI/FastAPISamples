from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm import declarative_base

# Step 1: Database Setup
# engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine("sqlite:///./relationships.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Step 2: Model Definitions
#############################################################################
# Association table for many-to-many relationship
student_course_association = Table(
    "student_course",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("student.id")),
    Column("course_id", Integer, ForeignKey("course.id")),
)


# Student class for many-to-many relationship
class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True)
    courses = relationship(
        "Course", secondary=student_course_association, back_populates="students"
    )


# Course class for many-to-many relationship
class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, primary_key=True)
    students = relationship(
        "Student", secondary=student_course_association, back_populates="courses"
    )


#############################################################################
# Parent class for one-to-many/many-to-one relationship
class Parent(Base):
    __tablename__ = "parent"
    id = Column(Integer, primary_key=True)
    children = relationship("Child", back_populates="parent")


# Child class for one-to-many/many-to-one relationship
class Child(Base):
    __tablename__ = "child"
    id = Column(Integer, primary_key=True)
    parent_id = Column(Integer, ForeignKey("parent.id"))
    parent = relationship("Parent", back_populates="children")


#############################################################################
# User class for one-to-one relationship
class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    profile = relationship("Profile", back_populates="user", uselist=False)


# Profile class for one-to-one relationship
class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True)
    profile_name = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="profile")


# Step 3: Creating the Database
Base.metadata.create_all(engine)

# Step 4: Adding Test Data

#############################
# Adding Students and Courses
student1 = Student()
student2 = Student()
course1 = Course()
course2 = Course()
student1.courses.append(course1)
student2.courses.append(course2)
session.add_all([student1, student2, course1, course2])

#############################
# Adding Parent and Children
parent1 = Parent()
child1 = Child(parent=parent1)
child2 = Child(parent=parent1)
session.add_all([parent1, child1, child2])


#############################
# Adding User and Profile
user1 = User(username="User1")
profile1 = Profile(user=user1)
session.add_all([user1, profile1])

session.commit()

# Step 5: Querying and Displaying Results

# Query for Parent-Child relationship
parents = session.query(Parent).all()
for parent in parents:
    print(f"Parent ID: {parent.id}, Number of children: {len(parent.children)}")

# Query for Student-Course relationship
students = session.query(Student).all()
for student in students:
    print(f"Student ID: {student.id}, Number of courses: {len(student.courses)}")

# Query for User-Profile relationship
users = session.query(User).all()
for user in users:
    print(f"User ID: {user.id}, Profile name: {user.profile.profile_name}")
