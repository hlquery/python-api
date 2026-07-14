"""
hlquery Python Client - Runtime Modules API
"""

from .service import Service


class Modules(Service):
    """Runtime module discovery and dynamic route helper."""

    def list(self):
        return self.client.execute_request("GET", "/modules")

    def load(self, name):
        self.require_non_empty_string(name, "Module name")
        return self.client.execute_request("POST", f"/loadmodule/{self.quote(name)}")

    def unload(self, name):
        self.require_non_empty_string(name, "Module name")
        return self.client.execute_request("POST", f"/unloadmodule/{self.quote(name)}")

    def syntax(self, name, params=None):
        self.require_non_empty_string(name, "Module name")
        return self.client.execute_request("GET", f"/modules/{self.quote(name)}/syntax", query_params=params or {})

    def call(self, name, route="", method="GET", body=None, query_params=None):
        self.require_non_empty_string(name, "Module name")
        method = str(method).upper()
        route = str(route or "").strip("/")
        path = f"/modules/{self.quote(name)}"
        if route:
            path += "/" + route
        return self.client.execute_request(method, path, body=body, query_params=query_params or {})
