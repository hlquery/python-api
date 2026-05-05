"""
hlquery Python Client - SAM API
"""

from .service import Service
from utils.validator import Validator


class SAM(Service):
    """SAM API helper."""

    def search(self, collection_name, query, params=None):
        Validator.validate_collection_name(collection_name)
        query_params = dict(params or {})
        query_params["collection"] = collection_name
        query_params["q"] = str(query)
        return self.client.execute_request("GET", "/sam/search", query_params=query_params)

    def status(self, collection_name=None, params=None):
        query_params = dict(params or {})

        if collection_name:
            Validator.validate_collection_name(collection_name)
            query_params["collection"] = collection_name

        return self.client.execute_request("GET", "/sam/status", query_params=query_params)

    def history(self, collection_name=None, limit=100, params=None):
        query_params = dict(params or {})
        query_params["limit"] = int(limit)

        if collection_name:
            Validator.validate_collection_name(collection_name)
            query_params["collection"] = collection_name

        return self.client.execute_request("GET", "/sam/history", query_params=query_params)
