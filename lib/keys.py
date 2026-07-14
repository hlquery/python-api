"""
hlquery Python Client - API Keys
"""

from .service import Service


class Keys(Service):
    """API key management helper."""

    def list(self):
        return self.client.execute_request("GET", "/keys")

    def get(self, key_id):
        self.require_non_empty_string(key_id, "Key ID")
        return self.client.execute_request("GET", f"/keys/{self.quote(key_id)}")

    def create(self, payload):
        return self.client.execute_request("POST", "/keys", body=payload or {})

    def update(self, key_id, payload):
        self.require_non_empty_string(key_id, "Key ID")
        return self.client.execute_request("PUT", f"/keys/{self.quote(key_id)}", body=payload or {})

    def delete(self, key_id):
        self.require_non_empty_string(key_id, "Key ID")
        return self.client.execute_request("DELETE", f"/keys/{self.quote(key_id)}")
