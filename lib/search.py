"""
hlquery Python Client - Search API
"""

from .service import Service
from utils.validator import Validator


class Search(Service):
    """Search API helper."""

    def search(self, collection_name, params):
        Validator.validate_collection_name(collection_name)
        Validator.validate_search_params(params or {})
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/search",
            query_params=params or {},
        )

    def vector_search(self, collection_name, params):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/vector_search",
            query_params=params or {},
        )

    def multi_search(self, searches):
        return self.client.execute_request(
            "POST",
            "/multi_search",
            body={"searches": searches or []},
        )

    def sql(self, collection_name, sql, params=None):
        Validator.validate_collection_name(collection_name)
        query_params = dict(params or {})
        query_params["sql"] = str(sql)
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/search",
            query_params=query_params,
        )


def urllib_parse_quote(value):
    from urllib.parse import quote
    return quote(str(value), safe="")
