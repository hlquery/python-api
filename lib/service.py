"""
hlquery Python Client - Base service
"""


class Service:
    """Base service wrapper."""

    def __init__(self, client):
        self.client = client
