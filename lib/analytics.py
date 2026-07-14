"""
hlquery Python Client - Analytics API
"""

from .service import Service


class Analytics(Service):
    """Analytics event helper."""

    def click(self, payload):
        return self.client.execute_request("POST", "/analytics/click", body=payload or {})
