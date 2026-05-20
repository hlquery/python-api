"""
hlquery Python Client - PDF parsing helper

Copyright (C) 2021-2026, Carlos F. Ferry <carlos.ferry@gmail.com>

This file is part of hlquery, released under the BSD License version 3.
"""

import hashlib
import json
import os
import re

try:
    from ..lib.exceptions import ValidationException
except (ImportError, ValueError):
    from lib.exceptions import ValidationException


class PDFParser:
    """Helper for parsing local PDF files into hlquery documents."""

    @staticmethod
    def parse_file(file_path, options=None):
        if options is None:
            options = {}

        PDFParser._validate_file_path(file_path)

        resolved_path = os.path.abspath(file_path)
        if not os.path.isfile(resolved_path):
            raise ValidationException(f"PDF path is not a file: {resolved_path}")

        reader_cls = PDFParser._load_pdf_reader()
        with open(resolved_path, 'rb') as handle:
            reader = reader_cls(handle)
            pages = []
            for page in reader.pages:
                text = page.extract_text() or ''
                pages.append(text)

            content = PDFParser.normalize_text('\n\n'.join(pages), options)
            metadata = {}
            raw_metadata = getattr(reader, 'metadata', None) or {}
            for key, value in dict(raw_metadata).items():
                normalized_key = str(key).lstrip('/')
                metadata[normalized_key] = PDFParser.normalize_metadata_value(value, options)

        title = PDFParser.resolve_title(resolved_path, metadata, options)

        return {
            'file_path': resolved_path,
            'file_name': os.path.basename(resolved_path),
            'title': title,
            'content': content,
            'page_count': len(pages),
            'metadata': metadata,
            'size_bytes': os.path.getsize(resolved_path)
        }

    @staticmethod
    def build_document_from_parsed_pdf(parsed, options=None):
        if options is None:
            options = {}

        content_field = options.get('content_field', 'content')
        title_field = options.get('title_field', 'title')
        document = dict(options.get('document', {}))

        document['id'] = options.get('id') or document.get('id') or PDFParser.generate_document_id(parsed['file_name'])
        document[title_field] = options.get('title') or document.get(title_field) or parsed['title']
        document[content_field] = parsed['content']

        if options.get('include_metadata', True):
            document['file_name'] = parsed['file_name']
            document['file_path'] = parsed['file_path']
            document['mime_type'] = 'application/pdf'
            document['page_count'] = str(parsed['page_count'])
            document['file_size_bytes'] = str(parsed['size_bytes'])
            PDFParser.attach_metadata(document, parsed.get('metadata', {}), options)

        return document

    @staticmethod
    def attach_metadata(document, metadata, options=None):
        if options is None:
            options = {}

        prefix = options.get('metadata_prefix', 'pdf_meta')

        for key, value in metadata.items():
            if value in (None, ''):
                continue

            normalized_key = PDFParser.normalize_field_name(f'{prefix}_{key}')
            if normalized_key:
                document[normalized_key] = value

    @staticmethod
    def normalize_metadata_value(value, options=None):
        if isinstance(value, (str, int, float, bool)):
            return PDFParser.normalize_text(str(value), options)

        return PDFParser.normalize_text(json.dumps(value, default=str), options)

    @staticmethod
    def normalize_field_name(name):
        normalized = re.sub(r'[^a-z0-9_]+', '_', str(name).strip().lower())
        normalized = normalized.strip('_')
        return normalized[:64]

    @staticmethod
    def normalize_text(text, options=None):
        if options is None:
            options = {}

        output = str(text or '').replace('\r\n', '\n').replace('\x00', '')

        if options.get('sanitize_commas', True):
            output = output.replace(',', ' ')

        if options.get('collapse_whitespace', True):
            output = re.sub(r'[ \t]+', ' ', output)
            output = re.sub(r'\n{3,}', '\n\n', output)

        return output.strip()

    @staticmethod
    def resolve_title(file_path, metadata, options=None):
        if options is None:
            options = {}

        if options.get('title'):
            return PDFParser.normalize_text(options['title'], options)

        metadata_title = metadata.get('Title') or metadata.get('title')
        if metadata_title:
            return PDFParser.normalize_text(metadata_title, options)

        return PDFParser.normalize_text(os.path.splitext(os.path.basename(file_path))[0], options)

    @staticmethod
    def generate_document_id(file_name):
        stem = os.path.splitext(os.path.basename(file_name))[0].lower()
        stem = re.sub(r'[^a-z0-9._-]+', '_', stem).strip('_')[:40]
        digest = hashlib.sha1(file_name.encode('utf-8')).hexdigest()[:8]
        return f"{stem or 'pdf'}_{digest}"

    @staticmethod
    def _validate_file_path(file_path):
        if not file_path or not isinstance(file_path, str):
            raise ValidationException("PDF file path must be a non-empty string")

    @staticmethod
    def _load_pdf_reader():
        try:
            from PyPDF2 import PdfReader
            return PdfReader
        except ImportError as error:
            raise ValidationException(
                "PDF parsing requires `PyPDF2`. Install the package dependencies with `pip install -e .`."
            ) from error
