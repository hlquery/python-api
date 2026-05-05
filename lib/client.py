"""
hlquery Python Client - Main client
"""

from .collections import Collections
from .documents import Documents
from .exceptions import ValidationException
from .request import Request
from .sam import SAM
from .search import Search
from .sql import SQL
from utils.auth import Auth
from utils.config import Config


class Client:
    """Main hlquery client."""

    def __init__(self, base_url=None, options=None):
        merged_options = Config.merge_defaults(options or {})
        resolved_base_url = base_url or merged_options["base_url"]

        if not Config.is_valid_url(resolved_base_url):
            raise ValidationException("Base URL must be a valid URL")

        self.base_url = Config.normalize_url(resolved_base_url)
        self.options = merged_options
        self.options["base_url"] = self.base_url
        self._request = Request(
            self.base_url,
            self.options.get("timeout", 30),
            self.options.get("token"),
            self.options.get("auth_method", "bearer"),
        )
        self._collections = None
        self._documents = None
        self._search = None
        self._sql = None
        self._sam = None

    def set_auth_token(self, token, auth_method="bearer"):
        if not Auth.is_valid_token(token):
            raise ValidationException("Authentication token must be a non-empty string")

        self.options["token"] = token
        self.options["auth_method"] = auth_method or "bearer"
        self._request.set_auth_token(token, self.options["auth_method"])
        return self

    def clear_auth(self):
        self.options["token"] = None
        self._request.clear_auth()
        return self

    def execute_request(self, method, path, body=None, query_params=None):
        return self._request.execute(method, path, body, query_params)

    def health(self):
        return self.execute_request("GET", "/health")

    def info(self):
        return self.execute_request("GET", "/")

    def stats(self):
        return self.execute_request("GET", "/stats")

    def collections_api(self):
        if self._collections is None:
            self._collections = Collections(self)
        return self._collections

    def documents_api(self):
        if self._documents is None:
            self._documents = Documents(self)
        return self._documents

    def search_api(self):
        if self._search is None:
            self._search = Search(self)
        return self._search

    def sql_api(self):
        if self._sql is None:
            self._sql = SQL(self)
        return self._sql

    def sam(self):
        if self._sam is None:
            self._sam = SAM(self)
        return self._sam

    def list_collections(self, offset=0, limit=10):
        return self.collections_api().list(offset, limit)

    def get_collection(self, collection_name):
        return self.collections_api().get(collection_name)

    def get_collection_fields(self, collection_name):
        return self.collections_api().get_fields(collection_name)

    def list_documents(self, collection_name, params=None):
        return self.documents_api().list(collection_name, params or {})

    def get_document(self, collection_name, document_id):
        return self.documents_api().get(collection_name, document_id)

    def search(self, collection_name, params):
        return self.search_api().search(collection_name, params)

    def sam_search(self, collection_name, query, params=None):
        return self.sam().search(collection_name, query, params or {})

    def sam_status(self, collection_name=None, params=None):
        return self.sam().status(collection_name, params or {})

    def sam_history(self, collection_name=None, limit=100, params=None):
        return self.sam().history(collection_name, limit, params or {})
