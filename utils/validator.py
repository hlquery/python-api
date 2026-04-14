"""
hlquery Python Client - Input Validation

Copyright (C) 2021-2026, Carlos F. Ferry <carlos.ferry@gmail.com>

This file is part of hlquery, released under the BSD License version 3.
"""

import re

# Import exceptions - handle both package and direct execution
try:
    from ..lib.exceptions import ValidationException
except (ImportError, ValueError):
    # Fallback for when running as script
    from lib.exceptions import ValidationException


class Validator:
    """Input validation utility class"""
    
    @staticmethod
    def validate_collection_name(name):
        """
        Validate collection name
        
        Args:
            name: Collection name string
        
        Raises:
            ValidationException: If validation fails
        """
        if not name or not isinstance(name, str):
            raise ValidationException("Collection name must be a non-empty string")
        
        # Check name length (matches server validation: 1-64 characters)
        if len(name) > 64:
            raise ValidationException("Collection name must be between 1 and 64 characters")
        
        # Collection names should be URL-safe
        if re.search(r'[^a-zA-Z0-9_-]', name):
            raise ValidationException(
                "Collection name contains invalid characters. "
                "Use only letters, numbers, underscores, and hyphens"
            )
        
        # Check if name starts with letter or underscore (matches server validation)
        if not name[0].isalpha() and name[0] != '_':
            raise ValidationException("Collection name must start with a letter or underscore")
    
    @staticmethod
    def validate_document_id(doc_id):
        """
        Validate document ID
        
        Args:
            doc_id: Document ID string
        
        Raises:
            ValidationException: If validation fails
        """
        if not doc_id or not isinstance(doc_id, str):
            raise ValidationException("Document ID must be a non-empty string")
        
        # Check name length (matches server validation: 1-64 characters)
        if len(doc_id) > 64:
            raise ValidationException("Document ID must be between 1 and 64 characters")
        
        # Document IDs should be URL-safe: alphanumeric, underscores, and hyphens only
        if re.search(r'[^a-zA-Z0-9_-]', doc_id):
            raise ValidationException(
                "Document ID contains invalid characters. "
                "Use only letters, numbers, underscores, and hyphens"
            )
    
    @staticmethod
    def validate_pagination(offset, limit):
        """
        Validate pagination parameters
        
        Args:
            offset: Offset integer
            limit: Limit integer
        
        Raises:
            ValidationException: If validation fails
        """
        if not isinstance(offset, int) or offset < 0:
            raise ValidationException("Offset must be a non-negative integer")
        
        if not isinstance(limit, int) or limit < 1:
            raise ValidationException("Limit must be a positive integer")
        
        if limit > 1000:
            raise ValidationException("Limit cannot exceed 1000")
    
    @staticmethod
    def validate_search_params(params):
        """
        Validate search parameters
        
        Args:
            params: Search parameters dictionary
        
        Raises:
            ValidationException: If validation fails
        """
        if 'limit' in params:
            limit = params['limit']
            if not isinstance(limit, int) or limit < 1:
                raise ValidationException("Limit must be a positive integer")
        
        if 'offset' in params:
            offset = params['offset']
            if not isinstance(offset, int) or offset < 0:
                raise ValidationException("Offset must be a non-negative integer")
        
        if 'page' in params:
            page = params['page']
            if not isinstance(page, int) or page < 1:
                raise ValidationException("Page must be a positive integer")
    
    @staticmethod
    def validate_document_fields(document):
        """
        Validate document field values for invalid characters
        Commas are not allowed in string field values as they're reserved for internal parsing
        
        Args:
            document: Document object to validate
        
        Raises:
            ValidationException: If document contains invalid characters
        """
        if not document or not isinstance(document, dict):
            return  # Skip validation for non-dict objects (will be validated per-item for arrays)
        
        for key, value in document.items():
            # Skip the 'id' field as it has its own validation
            if key == 'id':
                continue
            
            # Check string values for commas
            if isinstance(value, str) and ',' in value:
                raise ValidationException(
                    f"Field '{key}' contains invalid character: comma (`,`). "
                    f"Commas are not allowed in field values. Use underscores (_) or spaces instead, or use arrays for multiple values."
                )
            
            # Check array values - ensure they don't contain strings with commas
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, str) and ',' in item:
                        raise ValidationException(
                            f"Field '{key}' contains invalid character: comma (`,`). "
                            f"Array items cannot contain commas. Use underscores (_) or spaces instead."
                        )
