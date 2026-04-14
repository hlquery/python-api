"""
hlquery Python Client - Authentication Utilities

Copyright (C) 2021-2026, Carlos F. Ferry <carlos.ferry@gmail.com>

This file is part of hlquery, released under the BSD License version 3.
"""

import hashlib


class Auth:
    """Authentication utility class"""
    
    @staticmethod
    def generate_token(token):
        """
        Generate MD5 hash for token (utility function for token generation)
        Note: Authentication only requires a token - no username/password needed
        
        Args:
            token: Token string
        
        Returns:
            MD5 hash string
        """
        return hashlib.md5(token.encode('utf-8')).hexdigest()
    
    @staticmethod
    def is_valid_token(token):
        """
        Validate token format
        
        Args:
            token: Token string
        
        Returns:
            True if valid, False otherwise
        """
        return token and isinstance(token, str) and len(token) > 0
    
    @staticmethod
    def get_auth_header(token, method='bearer'):
        """
        Get authentication header value
        
        Args:
            token: Token string
            method: 'bearer' or 'api-key'
        
        Returns:
            Dictionary with 'header' and 'value' keys
        """
        if method == 'api-key':
            return {'header': 'X-API-Key', 'value': token}
        return {'header': 'Authorization', 'value': 'Bearer ' + token}
