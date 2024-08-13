#!/usr/bin/env python3
"""A Hash password method.
"""

import bcrypt

def _hash_password(password: str) -> bytes:
    """Hash a password using bcrypt.

    Args:
        password (str): The password to hash.

    Returns:
        bytes: The salted hash of the password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salt)
    return hashed_password
