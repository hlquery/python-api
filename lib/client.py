"""
hlquery Python Client - Main client
"""

from .collections import Collections
from .aliases import Aliases
from .analytics import Analytics
from .documents import Documents
from .exceptions import ValidationException
from .keys import Keys
from .links import Links
from .modules import Modules
from .overrides import Overrides
from .presets import Presets
from .request import Request
from .search import Search
from .sql import SQL
from .stopwords import Stopwords
from .synonyms import Synonyms
from .system import System
from .users import Users
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
        self._aliases = None
        self._analytics = None
        self._keys = None
        self._links = None
        self._modules = None
        self._overrides = None
        self._presets = None
        self._stopwords = None
        self._synonyms = None
        self._system = None
        self._users = None

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
        return self.system_api().health()

    def info(self):
        return self.system_api().info()

    def stats(self):
        return self.system_api().stats()

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

    def aliases_api(self):
        if self._aliases is None:
            self._aliases = Aliases(self)
        return self._aliases

    def analytics_api(self):
        if self._analytics is None:
            self._analytics = Analytics(self)
        return self._analytics

    def keys_api(self):
        if self._keys is None:
            self._keys = Keys(self)
        return self._keys

    def links_api(self):
        if self._links is None:
            self._links = Links(self)
        return self._links

    def modules_api(self):
        if self._modules is None:
            self._modules = Modules(self)
        return self._modules

    def overrides_api(self):
        if self._overrides is None:
            self._overrides = Overrides(self)
        return self._overrides

    def presets_api(self):
        if self._presets is None:
            self._presets = Presets(self)
        return self._presets

    def stopwords_api(self):
        if self._stopwords is None:
            self._stopwords = Stopwords(self)
        return self._stopwords

    def synonyms_api(self):
        if self._synonyms is None:
            self._synonyms = Synonyms(self)
        return self._synonyms

    def system_api(self):
        if self._system is None:
            self._system = System(self)
        return self._system

    def users_api(self):
        if self._users is None:
            self._users = Users(self)
        return self._users

    def list_collections(self, offset=0, limit=10):
        return self.collections_api().list(offset, limit)

    def get_collection(self, collection_name):
        return self.collections_api().get(collection_name)

    def get_collection_fields(self, collection_name):
        return self.collections_api().get_fields(collection_name)

    def get_collection_language(self, collection_name):
        return self.collections_api().language(collection_name)

    def list_collections_distributed(self, params=None):
        return self.collections_api().distributed(params or {})

    def list_documents(self, collection_name, params=None):
        return self.documents_api().list(collection_name, params or {})

    def get_document(self, collection_name, document_id):
        return self.documents_api().get(collection_name, document_id)

    def add_document(self, collection_name, document):
        return self.documents_api().add(collection_name, document)

    def update_document(self, collection_name, document_id, document):
        return self.documents_api().update(collection_name, document_id, document)

    def delete_document(self, collection_name, document_id):
        return self.documents_api().delete(collection_name, document_id)

    def add_pdf_document(self, collection_name, file_path, options=None):
        return self.documents_api().add_pdf(collection_name, file_path, options or {})

    def search(self, collection_name, params):
        return self.search_api().search(collection_name, params)

    def vector_search(self, collection_name, params, method="GET"):
        return self.search_api().vector_search(collection_name, params, method)

    def multi_search(self, searches):
        return self.search_api().multi_search(searches)

    def global_search(self, params=None, method="GET"):
        return self.search_api().global_search(params or {}, method)

    def search_all(self, params=None, method="GET"):
        return self.search_api().search_all(params or {}, method)

    def ping(self):
        return self.system_api().ping()

    def metrics(self):
        return self.system_api().metrics()

    def ready(self):
        return self.system_api().ready()

    def status(self):
        return self.system_api().status()
