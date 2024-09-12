import re
from datetime import datetime
from typing import Tuple, Union

from typing import Tuple, Optional


def validate_string_length(
    value: Optional[str], min_len: Optional[int] = None, max_len: Optional[int] = None
) -> Tuple[bool, str]:
    """
    Validates that the length of the string is within the optional min_len and max_len range.

    Args:
        value (Optional[str]): The string to validate.
        min_len (Optional[int]): The minimum allowed length (inclusive). Default is None.
        max_len (Optional[int]): The maximum allowed length (inclusive). Default is None.

    Returns:
        Tuple[bool, str]: A tuple where the first value is a boolean indicating if validation passed,
                          and the second value is an error message if validation failed.
    """
    if value is None:
        return False, "String value is required."

    value_len = len(value)

    if min_len is not None and max_len is not None:
        if value_len < min_len or value_len > max_len:
            return (
                False,
                f"String length must be between {min_len} and {max_len} characters.",
            )

    if min_len is not None and value_len < min_len:
        return False, f"String is too short. Minimum length is {min_len} characters."

    if max_len is not None and value_len > max_len:
        return False, f"String is too long. Maximum length is {max_len} characters."

    return True, "String length is valid."


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
