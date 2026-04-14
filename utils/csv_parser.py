"""
hlquery Python Client - CSV parsing helper

Copyright (C) 2021-2026, Carlos F. Ferry <carlos.ferry@gmail.com>

This file is part of hlquery, released under the BSD License version 3.
"""

import csv
import hashlib
import os
import re

try:
    from ..lib.exceptions import ValidationException
except (ImportError, ValueError):
    from lib.exceptions import ValidationException


class CSVParser:
    """Helper for parsing local CSV files into hlquery documents."""

    @staticmethod
    def parse_file(file_path, options=None):
        if options is None:
            options = {}

        CSVParser._validate_file_path(file_path)

        resolved_path = os.path.abspath(file_path)
        if not os.path.isfile(resolved_path):
            raise ValidationException(f"CSV path is not a file: {resolved_path}")

        delimiter = options.get('delimiter', ',')
        with open(resolved_path, 'r', encoding=options.get('encoding', 'utf-8'), newline='') as handle:
            rows = list(csv.reader(handle, delimiter=delimiter))

        header = rows[0] if rows else []
        data_rows = rows[1:] if len(rows) > 1 else []
        content_rows = data_rows if data_rows else rows
        content = CSVParser.normalize_rows(content_rows, options)

        return {
            'file_path': resolved_path,
            'file_name': os.path.basename(resolved_path),
            'title': CSVParser.resolve_title(resolved_path, options),
            'content': content,
            'row_count': len(data_rows) if data_rows else len(rows),
            'column_count': len(header) if header else (len(rows[0]) if rows else 0),
            'header': header,
            'size_bytes': os.path.getsize(resolved_path)
        }

    @staticmethod
    def build_document_from_parsed_csv(parsed, options=None):
        if options is None:
            options = {}

        content_field = options.get('content_field', 'content')
        title_field = options.get('title_field', 'title')
        document = dict(options.get('document', {}))

        document['id'] = options.get('id') or document.get('id') or CSVParser.generate_document_id(parsed['file_name'])
        document[title_field] = options.get('title') or document.get(title_field) or parsed['title']
        document[content_field] = parsed['content']
        document['file_name'] = parsed['file_name']
        document['file_path'] = parsed['file_path']
        document['mime_type'] = 'text/csv'
        document['row_count'] = str(parsed['row_count'])
        document['column_count'] = str(parsed['column_count'])

        if parsed['header']:
            document['columns'] = [CSVParser.normalize_text(value, options) for value in parsed['header']]

        return document

    @staticmethod
    def normalize_rows(rows, options=None):
        if options is None:
            options = {}

        lines = []
        for row in rows:
            cells = [CSVParser.normalize_text(cell, options) for cell in row]
            line = ' '.join([cell for cell in cells if cell])
            if line:
                lines.append(line)

        return '\n'.join(lines).strip()

    @staticmethod
    def normalize_text(text, options=None):
        if options is None:
            options = {}

        output = str(text or '').replace('\r\n', '\n').replace('\x00', '')
        output = output.replace(',', ' ')

        if options.get('collapse_whitespace', True):
            output = re.sub(r'[ \t]+', ' ', output)
            output = re.sub(r'\n{3,}', '\n\n', output)

        return output.strip()

    @staticmethod
    def resolve_title(file_path, options=None):
        if options is None:
            options = {}

        if options.get('title'):
            return CSVParser.normalize_text(options['title'], options)

        return CSVParser.normalize_text(os.path.splitext(os.path.basename(file_path))[0], options)

    @staticmethod
    def generate_document_id(file_name):
        stem = os.path.splitext(os.path.basename(file_name))[0].lower()
        stem = re.sub(r'[^a-z0-9._-]+', '_', stem).strip('_')[:40]
        digest = hashlib.sha1(file_name.encode('utf-8')).hexdigest()[:8]
        return f"{stem or 'csv'}_{digest}"

    @staticmethod
    def _validate_file_path(file_path):
        if not file_path or not isinstance(file_path, str):
            raise ValidationException("CSV file path must be a non-empty string")
