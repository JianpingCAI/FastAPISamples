# api_utils.py

import logging
from openapi_client.exceptions import ApiException, NotFoundException, UnauthorizedException

def handle_api_exception(e):
    """Handle exceptions raised by the OpenAPI client in a consistent way."""
    if isinstance(e, NotFoundException):
        logging.error("User not found: %s", e)
        # Return None or handle the 404 case
        return None

    elif isinstance(e, UnauthorizedException):
        logging.error("Unauthorized access: %s", e)
        # Raise an exception or notify the user
        raise UnauthorizedException("Unauthorized access. Please check your credentials.") from e

    elif isinstance(e, ApiException):
        logging.error("API error occurred. Status: %d, Reason: %s, Body: %s", e.status, e.reason, e.body)
        # Handle general API errors based on status
        if e.status == 500:
            logging.error("Server error. Retry later or escalate.")
            # Implement retry or return an error code
            return None
        else:
            # Raise or handle other types of API errors
            raise ApiException(f"API error: {e.reason}") from e

    else:
        logging.error("An unexpected error occurred: %s", e)
        # Optionally re-raise or return a fallback response
        raise e

# api_utils.py

from functools import wraps

def api_exception_handler(func):
    """Decorator to handle API exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return handle_api_exception(e)
    return wrapper

