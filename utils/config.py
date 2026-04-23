"""
hlquery Python Client - Configuration Utilities

Copyright (C) 2021-2026, Carlos F. Ferry <carlos.ferry@gmail.com>

This file is part of hlquery, released under the BSD License version 3.
"""

import os
from urllib.parse import urlparse


class Config:
    """Configuration utility class"""
    
    DEFAULT_TIMEOUT = 30
    DEFAULT_BASE_URL = os.environ.get('HLQ_BASE_URL') or os.environ.get('HLQUERY_BASE_URL') or 'http://localhost:9200'
    DEFAULT_AUTH_METHOD = 'bearer'
    
    @staticmethod
    def merge_defaults(user_options=None):
        """
        Merge user options with defaults
        
        Args:
            user_options: Dictionary of user options
        
        Returns:
            Dictionary with merged options
        """
        if user_options is None:
            user_options = {}
        
        defaults = {
            'timeout': Config.DEFAULT_TIMEOUT,
            'base_url': Config.DEFAULT_BASE_URL,
            'auth_method': Config.DEFAULT_AUTH_METHOD,
            'token': None
        }
        
        defaults.update(user_options)
        return defaults
    
    @staticmethod
    def is_valid_url(url):
        """
        Validate base URL
        
        Args:
            url: URL string to validate
        
        Returns:
            True if valid URL, False otherwise
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False
    
    @staticmethod
    def normalize_url(url):
        """
        Normalize base URL (remove trailing slash)
        
        Args:
            url: URL string
        
        Returns:
            Normalized URL string
        """
        return url.rstrip('/')
