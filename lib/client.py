from .collections import Collections
from .documents import Documents
from .request import Request
from .search import Search


class Client:
    def __init__(self, base_url, options=None):
        self._request = Request(base_url, options or {})
        self._collections = Collections(self._request)
        self._documents = Documents(self._request)
        self._search = Search(self._request)

    def set_auth_token(self, token, method="bearer"):
        self._request.set_auth_token(token, method)
        return self

    def execute_request(self, method, path, body=None, query_params=None, headers=None):
        return self._request.execute(method, path, payload=body, query_params=query_params, headers=headers)

    def health(self):
        return self.execute_request("GET", "/health")

    def stats(self):
        return self.execute_request("GET", "/stats")

    def info(self):
        return self.execute_request("GET", "/")

    def etc(self):
        return self.execute_request("GET", "/etc")

    def status(self):
        return self.execute_request("GET", "/status")

    def flush(self):
        return self.execute_request("POST", "/flush")

    def collections_api(self):
        return self._collections

    def documents_api(self):
        return self._documents

    def search_api(self):
        return self._search

    def list_collections(self, offset=0, limit=10):
        return self._collections.list(offset, limit)

    def get_collection(self, name):
        return self._collections.get(name)

    def get_collection_fields(self, name):
        return self._collections.get_fields(name)

    def list_documents(self, collection, params=None):
        return self._documents.list(collection, params or {})

    def get_document(self, collection, document_id):
        return self._documents.get(collection, document_id)

    def search(self, collection, params=None):
        return self._search.search(collection, params or {})

    def vector_search(self, collection, params=None):
        return self._search.vector_search(collection, params or {})
