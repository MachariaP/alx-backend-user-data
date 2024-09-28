#!/usr/bin/env python3

"""This module defines the model for saving user sessions."""

from models.base import Base


class UserSession(Base):
    """Implement the user session model."""

    def __init__(
        self, user_id: str, session_id: str, *args: list, **kwargs: dict
    ):
        """Initialize user session object."""
        super().__init__(*args, **kwargs)
        self.user_id: str = user_id
        self.session_id: str = session_id
