"""
hlquery Python Client - Users API
"""

from .service import Service


class Users(Service):
    """User management helper."""

    def list(self):
        return self.client.execute_request("GET", "/users")

    def get(self, name):
        self.require_non_empty_string(name, "User name")
        return self.client.execute_request("GET", f"/users/{self.quote(name)}")

    def create(self, payload):
        return self.client.execute_request("POST", "/users", body=payload or {})

    def update(self, name, payload):
        self.require_non_empty_string(name, "User name")
        return self.client.execute_request("PUT", f"/users/{self.quote(name)}", body=payload or {})

    def delete(self, name):
        self.require_non_empty_string(name, "User name")
        return self.client.execute_request("DELETE", f"/users/{self.quote(name)}")
