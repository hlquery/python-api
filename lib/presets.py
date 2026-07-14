"""
hlquery Python Client - Presets API
"""

from .service import Service


class Presets(Service):
    """Search preset management helper."""

    def list(self):
        return self.client.execute_request("GET", "/presets")

    def get(self, name):
        self.require_non_empty_string(name, "Preset name")
        return self.client.execute_request("GET", f"/presets/{self.quote(name)}")

    def create(self, name, payload):
        self.require_non_empty_string(name, "Preset name")
        return self.client.execute_request("POST", f"/presets/{self.quote(name)}", body=payload or {})

    def update(self, name, payload):
        self.require_non_empty_string(name, "Preset name")
        return self.client.execute_request("PUT", f"/presets/{self.quote(name)}", body=payload or {})

    def upsert(self, name, payload):
        return self.create(name, payload)

    def delete(self, name):
        self.require_non_empty_string(name, "Preset name")
        return self.client.execute_request("DELETE", f"/presets/{self.quote(name)}")
