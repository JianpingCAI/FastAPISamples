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
from sqlalchemy.ext.declarative import declarative_base

# Step 1: Database Setup
# engine = create_engine('sqlite:///:memory:', echo=True)
# engine = create_engine("sqlite:///./relationships.db", echo=True)
engine = create_engine("duckdb:///./relationships.db", echo=True)
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
id_seq1 = Sequence("id_seq1")


class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, id_seq1, server_default=id_seq1.next_value(), primary_key=True)
    courses = relationship(
        "Course", secondary=student_course_association, back_populates="students"
    )


# Course class for many-to-many relationship
id_seq2 = Sequence("id_seq2")


class Course(Base):
    __tablename__ = "course"
    id = Column(Integer, id_seq2, server_default=id_seq2.next_value(), primary_key=True)
    students = relationship(
        "Student", secondary=student_course_association, back_populates="courses"
    )


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


session.commit()

# Step 5: Querying and Displaying Results

# Query for Student-Course relationship
students = session.query(Student).all()
for student in students:
    print(f"Student ID: {student.id}, Number of courses: {len(student.courses)}")

session.close()
