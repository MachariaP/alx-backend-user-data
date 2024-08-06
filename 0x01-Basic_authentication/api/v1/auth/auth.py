#!/usr/bin/env python3
"""
Auth class
"""

from flask import request
from typing import List, TypeVar

class Auth:
    """Authentication class.
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Determines if authentication is required.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True

        # Ensure path ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the authorization header from the request.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns the current user.
        """
        return None
