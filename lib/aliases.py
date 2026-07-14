"""
hlquery Python Client - Aliases API
"""

from .service import Service
from utils.validator import Validator


class Aliases(Service):
    """Alias management helper."""

    def list(self, params=None):
        return self.client.execute_request("GET", "/aliases", query_params=params or {})

    def list_collection(self, collection_name, params=None):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "GET",
            f"/collections/{self.quote(collection_name)}/aliases",
            query_params=params or {},
        )

    def get(self, alias):
        self.require_non_empty_string(alias, "Alias")
        return self.client.execute_request("GET", f"/aliases/{self.quote(alias)}")

    def create(self, alias, payload):
        self.require_non_empty_string(alias, "Alias")
        return self.client.execute_request("POST", f"/aliases/{self.quote(alias)}", body=payload or {})

    def update(self, alias, payload):
        self.require_non_empty_string(alias, "Alias")
        return self.client.execute_request("PUT", f"/aliases/{self.quote(alias)}", body=payload or {})

    def upsert(self, alias, payload):
        return self.create(alias, payload)

    def delete(self, alias):
        self.require_non_empty_string(alias, "Alias")
        return self.client.execute_request("DELETE", f"/aliases/{self.quote(alias)}")
