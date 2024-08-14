#!/usr/bin/env python3
""" Auth module.
"""
import uuid
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

    def valid_login(self, email: str, password: str) -> bool:
        """Validate login credentials.

        Args:
            email (str): The email of the user.
            password (str): The password of the user.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode(), user.hashed_password)
        except NoResultFound:
            return False

    @staticmethod
    def _generate_uuid() -> str:
        """Generate a new UUID and return its string representation.

        Returns:
            str: The string representatin of the generated UUID.
        """
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Create a session for the user with the given email.

        Args:
            email (str): The email of the user.

        Returns:
            str: The session ID as a string, or None if the user is not found.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """Get a user from a session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            User: The corresponding User object, or None if no user is found.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroy a user's session by setting their session ID to None.
        Args:
            user_id (int): The ID of the user.

        Returns:
            None
        """
        self._db.update_user(user_id, session_id=None)
        return None
