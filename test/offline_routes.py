import os
import sys
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from lib.client import Client


class RecordingRequest:
    def __init__(self):
        self.calls = []

    def execute(self, method, path, body=None, query_params=None):
        call = {
            "method": method,
            "path": path,
            "body": body,
            "query_params": query_params,
        }
        self.calls.append(call)
        return call


class PythonClientOfflineRouteTests(unittest.TestCase):
    def setUp(self):
        self.client = Client("http://localhost:9200")
        self.recorder = RecordingRequest()
        self.client._request = self.recorder

    def last_call(self):
        return self.recorder.calls[-1]

    def test_collection_update_uses_server_update_route(self):
        result = self.client.collections_api().update("books", {"searchable_fields": ["title"]})

        self.assertEqual(result["method"], "POST")
        self.assertEqual(result["path"], "/collections/books/update")
        self.assertEqual(result["body"], {"searchable_fields": ["title"]})

    def test_collection_fields_uses_collection_get_route(self):
        result = self.client.collections_api().get_fields("books")

        self.assertEqual(result["method"], "GET")
        self.assertEqual(result["path"], "/collections/books")

    def test_document_update_uses_put(self):
        result = self.client.documents_api().update("books", "doc_1", {"title": "Updated"})

        self.assertEqual(result["method"], "PUT")
        self.assertEqual(result["path"], "/collections/books/documents/doc_1")
        self.assertEqual(result["body"], {"title": "Updated"})

    def test_sql_exec_uses_exec_body_field(self):
        result = self.client.sql_api().exec("CREATE COLLECTION books")

        self.assertEqual(result["method"], "POST")
        self.assertEqual(result["path"], "/sql")
        self.assertEqual(result["body"], {"exec": "CREATE COLLECTION books"})

    def test_collection_language_uses_lang_route(self):
        result = self.client.collections_api().language("books")

        self.assertEqual(result["method"], "GET")
        self.assertEqual(result["path"], "/collections/books/lang")

    def test_update_by_query_uses_underscore_route(self):
        result = self.client.documents_api().update_by_query("books", {"filter_by": "id:=1"})

        self.assertEqual(result["method"], "POST")
        self.assertEqual(result["path"], "/collections/books/documents/_update_by_query")
        self.assertEqual(result["body"], {"filter_by": "id:=1"})

    def test_resource_group_routes(self):
        self.assertEqual(self.client.synonyms_api().list_global()["path"], "/synonyms/global")
        self.assertEqual(self.client.stopwords_api().list_global_stopword_set()["path"], "/stopword_sets/global")
        self.assertEqual(self.client.overrides_api().get_curation("books", "featured")["path"], "/collections/books/curations/featured")
        self.assertEqual(self.client.aliases_api().list_collection("books")["path"], "/collections/books/aliases")
        self.assertEqual(self.client.modules_api().syntax("demo")["path"], "/modules/demo/syntax")
        self.assertEqual(self.client.presets_api().get("default")["path"], "/presets/default")
        self.assertEqual(self.client.keys_api().get("key_1")["path"], "/keys/key_1")
        self.assertEqual(self.client.users_api().get("admin")["path"], "/users/admin")
        self.assertEqual(self.client.links_api().ping()["path"], "/links/ping")
        self.assertEqual(self.client.analytics_api().click({"collection": "books", "doc_id": "1"})["path"], "/analytics/click")


if __name__ == "__main__":
    unittest.main()
