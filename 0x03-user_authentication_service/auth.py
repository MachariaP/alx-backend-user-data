#!/usr/bin/env python3
""" Auth module.
"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


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


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user with the given email and password.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Raises:
            ValueError: If a user with the given email already exists.

        Returns:
            User: The newly created User object.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password=password)
            new_user = self._db.add_user(
                    email=email, hashed_password=hashed_password)
            return new_user
