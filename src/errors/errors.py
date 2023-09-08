"""Module for error handling."""
from typing import Any, Dict


class ApiError(Exception):
    """Base class for all of our API errors."""

    def __init__(self, status_code: int, error_code: str,
                 description: str) -> None:
        """Create an ApiError.

        Positional Arguments:
            status_code: HTTP status code
            error_code: Application error code
            description: Human description of the error code

        """
        Exception.__init__(self)
        self.status_code = status_code
        self.error_code = error_code
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        """Return a dict of all attributes."""
        return {
            'status': self.status_code,
            'error': self.error_code,
            'description': self.description
        }
