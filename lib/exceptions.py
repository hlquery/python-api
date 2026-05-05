"""
hlquery Python Client - Exceptions
"""


class HlqueryError(Exception):
    """Base client exception."""


class ValidationException(HlqueryError):
    """Raised when client-side validation fails."""
