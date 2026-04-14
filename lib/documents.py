import os
import urllib.parse

from utils.csv_parser import CSVParser
from utils.pdf_parser import PDFParser


class Documents:
    def __init__(self, request):
        self._request = request

    def list(self, collection, params=None):
        return self._request.execute("GET", f"/collections/{urllib.parse.quote(collection, safe='')}/documents", query_params=params or {})

    def get(self, collection, document_id):
        return self._request.execute("GET", f"/collections/{urllib.parse.quote(collection, safe='')}/documents/{urllib.parse.quote(document_id, safe='')}")

    def add(self, collection, document):
        return self._request.execute("POST", f"/collections/{urllib.parse.quote(collection, safe='')}/documents", payload=document)

    def update(self, collection, document_id, document):
        return self._request.execute("PUT", f"/collections/{urllib.parse.quote(collection, safe='')}/documents/{urllib.parse.quote(document_id, safe='')}", payload=document)

    def delete(self, collection, document_id):
        return self._request.execute("DELETE", f"/collections/{urllib.parse.quote(collection, safe='')}/documents/{urllib.parse.quote(document_id, safe='')}")

    def import_documents(self, collection, documents):
        return self._request.execute("POST", f"/collections/{urllib.parse.quote(collection, safe='')}/documents/import", payload={"documents": documents or []})

    def delete_by_filter(self, collection, filter_by):
        return self._request.execute(
            "DELETE",
            f"/collections/{urllib.parse.quote(collection, safe='')}/documents",
            query_params={"filter_by": filter_by},
        )

    def add_pdf(self, collection, file_path, options=None):
        options = options or {}
        parsed = PDFParser.parse_file(file_path, options)
        if not parsed:
            raise ValueError(f"Failed to parse PDF file: {file_path}")
        document = PDFParser.build_document_from_parsed_pdf(parsed, options)
        return self.add(collection, document)

    def add_csv(self, collection, file_path, options=None):
        options = options or {}
        parsed = CSVParser.parse_file(file_path, options)
        if not parsed:
            raise ValueError(f"Failed to parse CSV file: {file_path}")
        document = CSVParser.build_document_from_parsed_csv(parsed, options)
        return self.add(collection, document)
