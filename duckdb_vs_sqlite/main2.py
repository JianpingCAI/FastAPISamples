# Assuming models.py contains the defined models TestSuite, TestCase, and Tag
# from models_sqlite import engine, Base, TestSuite, TestCase, Tag
from models_duckdb import engine, Base, TestSuite, TestCase
from sqlalchemy.orm import sessionmaker

# Creating a session
Session = sessionmaker(bind=engine)
session = Session()

# # Function to create new entries
# def create_test_data():
#     new_suite = TestSuite(name="New Suite", description="A new test suite.")
#     new_case = TestCase(name="New Case", description="A new test case", expected_outcome="Pass")
#     new_tag = Tag(name="Critical", tag_type="TestCase")

#     # Adding relationships
#     new_suite.test_cases.append(new_case)
#     new_case.tags.append(new_tag)

#     # Adding to session and committing
#     session.add(new_suite)
#     session.commit()
#     print("Data created successfully.")

# # Function to read data
# def read_test_data():
#     suites = session.query(TestSuite).all()
#     for suite in suites:
#         print(f"TestSuite: {suite.name}, Description: {suite.description}")
#         for test_case in suite.test_cases:
#             print(f"\tTestCase: {test_case.name}, Expected Outcome: {test_case.expected_outcome}")
#             for tag in test_case.tags:
#                 print(f"\t\tTag: {tag.name}, Type: {tag.tag_type}")

# # Function to update data
# def update_test_data(test_suite_name, new_description):
#     suite = session.query(TestSuite).filter_by(name=test_suite_name).first()
#     if suite:
#         suite.description = new_description
#         session.commit()
#         print("TestSuite updated successfully.")
#     else:
#         print("TestSuite not found.")

# # Function to delete data
# def delete_test_data(test_suite_name):
#     suite = session.query(TestSuite).filter_by(name=test_suite_name).first()
#     if suite:
#         session.delete(suite)
#         session.commit()
#         print("TestSuite deleted successfully.")
#     else:
#         print("TestSuite not found.")

# Testing the functions
# create_test_data()
# read_test_data()
# update_test_data("New Suite", "Updated description for the new suite.")
# read_test_data()
# delete_test_data("New Suite")
# read_test_data()

# Closing the session
session.close()
