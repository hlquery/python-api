"""
hlquery Python Client - Base service
"""

from .exceptions import ValidationException


class Service:
    """Base service wrapper."""

    def __init__(self, client):
        self.client = client

    @staticmethod
    def quote(value):
        from urllib.parse import quote
        return quote(str(value), safe="")

    @staticmethod
    def require_non_empty_string(value, label):
        if not isinstance(value, str) or not value.strip():
            raise ValidationException(f"{label} must be a non-empty string")
