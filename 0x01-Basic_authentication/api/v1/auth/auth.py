#!/usr/bin/env python3
""" Auth class
"""

from flask import request
from typing import List, TypeVar


class Auth:
    def require_auth(self, path:str, executed_paths: List[str]) -> bool:
        """
        Determines if authentication is needed.
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header.
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user.
        """
        return None
