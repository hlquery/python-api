"""
hlquery Python Client - Documents API
"""

from .service import Service
from utils.pdf_parser import PDFParser
from utils.validator import Validator


class Documents(Service):
    """Documents API helper."""

    def list(self, collection_name, params=None):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/documents",
            query_params=params or {},
        )

    def get(self, collection_name, document_id):
        Validator.validate_collection_name(collection_name)
        Validator.validate_document_id(document_id)
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/{urllib_parse_quote(document_id)}",
        )

    def add(self, collection_name, document):
        Validator.validate_collection_name(collection_name)
        Validator.validate_document_fields(document)

        if isinstance(document, dict) and "id" in document:
            Validator.validate_document_id(document["id"])

        return self.client.execute_request(
            "POST",
            f"/collections/{urllib_parse_quote(collection_name)}/documents",
            body=document,
        )

    def add_pdf(self, collection_name, file_path, options=None):
        Validator.validate_collection_name(collection_name)

        parsed = PDFParser.parse_file(file_path, options or {})
        document = PDFParser.build_document_from_parsed_pdf(parsed, options or {})
        return self.add(collection_name, document)

    def update(self, collection_name, document_id, document):
        Validator.validate_collection_name(collection_name)
        Validator.validate_document_id(document_id)
        Validator.validate_document_fields(document)
        return self.client.execute_request(
            "PUT",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/{urllib_parse_quote(document_id)}",
            body=document,
        )

    def delete(self, collection_name, document_id):
        Validator.validate_collection_name(collection_name)
        Validator.validate_document_id(document_id)
        return self.client.execute_request(
            "DELETE",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/{urllib_parse_quote(document_id)}",
        )

    def import_documents(self, collection_name, documents, params=None):
        Validator.validate_collection_name(collection_name)

        for document in documents or []:
            Validator.validate_document_fields(document)

        return self.client.execute_request(
            "POST",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/import",
            body=documents or [],
            query_params=params or {},
        )

    def bulk_import(self, collection_name, documents, params=None):
        return self.import_documents(collection_name, documents, params)

    def delete_by_filter(self, collection_name, params):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "DELETE",
            f"/collections/{urllib_parse_quote(collection_name)}/documents",
            query_params=params or {},
        )

    def context(self, collection_name, document_id, params=None):
        Validator.validate_collection_name(collection_name)
        Validator.validate_document_id(document_id)
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/{urllib_parse_quote(document_id)}/context",
            query_params=params or {},
        )

    def update_by_query(self, collection_name, payload):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "POST",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/_update_by_query",
            body=payload or {},
        )

    def delete_by_query(self, collection_name, payload):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "POST",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/_delete_by_query",
            body=payload or {},
        )

    def search(self, collection_name, params):
        Validator.validate_collection_name(collection_name)
        Validator.validate_search_params(params or {})
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/search",
            query_params=params or {},
        )

    def search_post(self, collection_name, payload):
        Validator.validate_collection_name(collection_name)
        return self.client.execute_request(
            "POST",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/search",
            body=payload or {},
        )

    def facets(self, collection_name, params=None, method="GET"):
        Validator.validate_collection_name(collection_name)
        method = str(method).upper()
        if method == "POST":
            return self.client.execute_request(
                "POST",
                f"/collections/{urllib_parse_quote(collection_name)}/documents/facet_counts",
                body=params or {},
            )
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/facet_counts",
            query_params=params or {},
        )

    def export(self, collection_name, params=None, method="GET"):
        Validator.validate_collection_name(collection_name)
        method = str(method).upper()
        if method == "POST":
            return self.client.execute_request(
                "POST",
                f"/collections/{urllib_parse_quote(collection_name)}/documents/export",
                body=params or {},
            )
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/export",
            query_params=params or {},
        )

    def maybe(self, collection_name, params=None, method="GET"):
        Validator.validate_collection_name(collection_name)
        method = str(method).upper()
        if method == "POST":
            return self.client.execute_request(
                "POST",
                f"/collections/{urllib_parse_quote(collection_name)}/documents/maybe",
                body=params or {},
            )
        return self.client.execute_request(
            "GET",
            f"/collections/{urllib_parse_quote(collection_name)}/documents/maybe",
            query_params=params or {},
        )


def urllib_parse_quote(value):
    from urllib.parse import quote
    return quote(str(value), safe="")
