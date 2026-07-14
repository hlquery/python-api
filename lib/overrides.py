"""
hlquery Python Client - Overrides API
"""

from .service import Service
from utils.validator import Validator


class Overrides(Service):
    """Search override management helper."""

    def list(self, collection_name, params=None):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "GET",
            f"/collections/{self.quote(collection_name)}/overrides",
            query_params=params or {},
        )

    def list_curations(self, collection_name, params=None):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "GET",
            f"/collections/{self.quote(collection_name)}/curations",
            query_params=params or {},
        )

    def get(self, collection_name, override_id):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(override_id, "Override ID")
        return self.client.execute_request(
            "GET",
            f"/collections/{self.quote(collection_name)}/overrides/{self.quote(override_id)}",
        )

    def get_curation(self, collection_name, curation_id):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(curation_id, "Curation ID")
        return self.client.execute_request(
            "GET",
            f"/collections/{self.quote(collection_name)}/curations/{self.quote(curation_id)}",
        )

    def create(self, collection_name, override_id, payload):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(override_id, "Override ID")
        return self.client.execute_request(
            "POST",
            f"/collections/{self.quote(collection_name)}/overrides/{self.quote(override_id)}",
            body=payload or {},
        )

    def create_curation(self, collection_name, curation_id, payload):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(curation_id, "Curation ID")
        return self.client.execute_request(
            "POST",
            f"/collections/{self.quote(collection_name)}/curations/{self.quote(curation_id)}",
            body=payload or {},
        )

    def update(self, collection_name, override_id, payload):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(override_id, "Override ID")
        return self.client.execute_request(
            "PUT",
            f"/collections/{self.quote(collection_name)}/overrides/{self.quote(override_id)}",
            body=payload or {},
        )

    def update_curation(self, collection_name, curation_id, payload):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(curation_id, "Curation ID")
        return self.client.execute_request(
            "PUT",
            f"/collections/{self.quote(collection_name)}/curations/{self.quote(curation_id)}",
            body=payload or {},
        )

    def upsert(self, collection_name, override_id, payload):
        return self.create(collection_name, override_id, payload)

    def delete(self, collection_name, override_id):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(override_id, "Override ID")
        return self.client.execute_request(
            "DELETE",
            f"/collections/{self.quote(collection_name)}/overrides/{self.quote(override_id)}",
        )

    def delete_curation(self, collection_name, curation_id):
        Validator.validate_collection_name(collection_name)
        self.require_non_empty_string(curation_id, "Curation ID")
        return self.client.execute_request(
            "DELETE",
            f"/collections/{self.quote(collection_name)}/curations/{self.quote(curation_id)}",
        )
