"""
hlquery Python Client - Links API
"""

from .service import Service


class Links(Service):
    """Distributed links helper."""

    def list(self, params=None):
        return self.client.execute_request("GET", "/links", query_params=params or {})

    def ping(self, params=None):
        return self.client.execute_request("GET", "/links/ping", query_params=params or {})

    def connect(self, endpoint):
        self.require_non_empty_string(endpoint, "Endpoint")
        return self.client.execute_request("POST", "/links/connect", body={"endpoint": endpoint})

    def disconnect(self, endpoint):
        self.require_non_empty_string(endpoint, "Endpoint")
        return self.client.execute_request("POST", "/links/disconnect", body={"endpoint": endpoint})
