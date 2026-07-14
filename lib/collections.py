"""
hlquery Python Client - Collections API
"""

from .service import Service
from utils.validator import Validator


class Collections(Service):
    """Collections API helper."""

    def list(self, offset=0, limit=10):
        Validator.validate_pagination(int(offset), int(limit))

        return self.client.execute_request(
            "GET",
            "/collections",
            query_params={
                "offset": int(offset),
                "limit": int(limit),
            },
        )

    def distributed(self, params=None):
        return self.client.execute_request("GET", "/collections/distributed", query_params=params or {})

    def create(self, collection_name, schema):
        Validator.validate_collection_name(collection_name)
        payload = dict(schema or {})
        payload["name"] = collection_name
        return self.client.execute_request("POST", "/collections", body=payload)

    def get(self, collection_name):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request("GET", f"/collections/{urllib_parse_quote(collection_name)}")

    def get_fields(self, collection_name):
        Validator.validate_collection_name(collection_name)
        return self.get(collection_name)

    def language(self, collection_name):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/lang",
        )

    def vector_search(self, collection_name, params, method="GET"):
        Validator.validate_collection_name(collection_name)
        method = str(method).upper()
        if method == "POST":
            return self.client.execute_request(
                "POST",
                f"/collections/{urllib_parse_quote(collection_name)}/vector_search",
                body=params or {},
            )
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/vector_search",
            query_params=params or {},
        )

    def update(self, collection_name, schema):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "POST",
            f"/collections/{urllib_parse_quote(collection_name)}/update",
            body=schema or {},
        )

    def delete(self, collection_name):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request("DELETE", f"/collections/{urllib_parse_quote(collection_name)}")


def urllib_parse_quote(value):
    from urllib.parse import quote
    return quote(str(value), safe="")
