"""
hlquery Python Client - Stopwords API
"""

from .service import Service
from utils.validator import Validator


class Stopwords(Service):
    """Stopword management helper."""

    def list_all(self, params=None):
        return self.client.execute_request("GET", "/stopwords", query_params=params or {})

    def list_stopword_sets(self, params=None):
        return self.client.execute_request("GET", "/stopword_sets", query_params=params or {})

    def list(self, collection_name, params=None):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "GET",
            f"/collections/{self.quote(collection_name)}/stopwords",
            query_params=params or {},
        )

    def create(self, collection_name, payload):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request("POST", f"/collections/{self.quote(collection_name)}/stopwords", body=payload or {})

    def delete(self, collection_name, term):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(term, "Stopword")
        return self.client.execute_request("DELETE", f"/collections/{self.quote(collection_name)}/stopwords/{self.quote(term)}")

    def list_global(self, params=None):
        return self.client.execute_request("GET", "/stopwords/global", query_params=params or {})

    def list_global_stopword_set(self, params=None):
        return self.client.execute_request("GET", "/stopword_sets/global", query_params=params or {})

    def create_global(self, payload):
        return self.client.execute_request("POST", "/stopwords/global", body=payload or {})

    def create_in_global_stopword_set(self, payload):
        return self.client.execute_request("POST", "/stopword_sets/global", body=payload or {})

    def delete_global(self, term):
        self.require_non_empty_string(term, "Stopword")
        return self.client.execute_request("DELETE", f"/stopwords/global/{self.quote(term)}")

    def delete_from_global_stopword_set(self, term):
        self.require_non_empty_string(term, "Stopword")
        return self.client.execute_request("DELETE", f"/stopword_sets/global/items/{self.quote(term)}")
