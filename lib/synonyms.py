"""
hlquery Python Client - Synonyms API
"""

from .service import Service
from utils.validator import Validator


class Synonyms(Service):
    """Synonym management helper."""

    def list_all(self, params=None):
        return self.client.execute_request("GET", "/synonyms", query_params=params or {})

    def list_synonym_sets(self, params=None):
        return self.client.execute_request("GET", "/synonym_sets", query_params=params or {})

    def list(self, collection_name, params=None):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "GET",
            f"/collections/{self.quote(collection_name)}/synonyms",
            query_params=params or {},
        )

    def get(self, collection_name, term):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("GET", f"/collections/{self.quote(collection_name)}/synonyms/{self.quote(term)}")

    def create(self, collection_name, term, payload):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("POST", f"/collections/{self.quote(collection_name)}/synonyms/{self.quote(term)}", body=payload or {})

    def update(self, collection_name, term, payload):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("PUT", f"/collections/{self.quote(collection_name)}/synonyms/{self.quote(term)}", body=payload or {})

    def upsert(self, collection_name, term, payload):
        return self.create(collection_name, term, payload)

    def delete(self, collection_name, term):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("DELETE", f"/collections/{self.quote(collection_name)}/synonyms/{self.quote(term)}")

    def list_global(self, params=None):
        return self.client.execute_request("GET", "/synonyms/global", query_params=params or {})

    def list_global_synonym_set(self, params=None):
        return self.client.execute_request("GET", "/synonym_sets/global", query_params=params or {})

    def get_global(self, term):
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("GET", f"/synonyms/global/{self.quote(term)}")

    def get_from_global_synonym_set(self, term):
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("GET", f"/synonym_sets/global/items/{self.quote(term)}")

    def create_global(self, term, payload):
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("POST", f"/synonyms/global/{self.quote(term)}", body=payload or {})

    def create_in_global_synonym_set(self, term, payload):
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("POST", f"/synonym_sets/global/items/{self.quote(term)}", body=payload or {})

    def update_global(self, term, payload):
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("PUT", f"/synonyms/global/{self.quote(term)}", body=payload or {})

    def update_in_global_synonym_set(self, term, payload):
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("PUT", f"/synonym_sets/global/items/{self.quote(term)}", body=payload or {})

    def upsert_global(self, term, payload):
        return self.create_global(term, payload)

    def delete_global(self, term):
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("DELETE", f"/synonyms/global/{self.quote(term)}")

    def delete_from_global_synonym_set(self, term):
        self.require_non_empty_string(term, "Synonym term")
        return self.client.execute_request("DELETE", f"/synonym_sets/global/items/{self.quote(term)}")
