import re
from datetime import datetime
from typing import Tuple, Union


def validate_name(name: str) -> Tuple[bool, Union[str, None]]:
    """Validates that the name is at least 3 characters long."""
    if not name or len(name) < 3:
        return False, "Name must be at least 3 characters long."
    return True, None


def validate_age(age: Union[str, int]) -> Tuple[bool, Union[int, str]]:
    """Validates that the age is a positive number between 0 and 120."""
    try:
        age_value = int(age)
        if age_value < 0 or age_value > 120:
            return False, "Age must be between 0 and 120."
        return True, age_value
    except (ValueError, TypeError):
        return False, "Invalid age. Please enter a number."


def validate_email(email: str) -> Tuple[bool, Union[str, None]]:
    """Validates the email address format."""
    email_regex = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(email_regex, email):
        return False, "Invalid email format."
    return True, None


def validate_date_of_birth(dob: str) -> Tuple[bool, Union[datetime, str]]:
    """Validates the date of birth in YYYY-MM-DD format."""
    try:
        date = datetime.strptime(dob, "%Y-%m-%d")
        return True, date
    except ValueError:
        return False, "Invalid date format. Please use YYYY-MM-DD."


def validate_postal_code(postal_code: str) -> Tuple[bool, Union[str, None]]:
    """Validates postal code (optional)."""
    if postal_code and len(postal_code) < 5:
        return False, "Postal code must be at least 5 characters long."
    return True, None
