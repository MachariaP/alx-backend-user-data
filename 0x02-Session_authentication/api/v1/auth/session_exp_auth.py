#!/usr/bin/env python3

"""This module defines a class for expiring sessions"""
import os
from datetime import datetime, timedelta
from typing import Union

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Implement Session Expiry Authentication class."""

    def __init__(self):
        """Initialize the session expiration object."""
        super().__init__()
        try:
            self.session_duration = int(os.environ.get("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """Create an expirable session."""
        session_id = super().create_session(user_id=user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }

        return session_id

    def user_id_for_session_id(
        self, session_id: str = None
    ) -> Union[str, None]:
        """Return the User ID for the user who owns a given session ID."""
        if not session_id:
            return None

        session = self.user_id_by_session_id.get(session_id, {})

        if "created_at" not in session:
            return None

        if self.session_duration <= 0:  # non-expiry session
            return session.get("user_id")

        if (
            session.get("created_at")
            + timedelta(seconds=self.session_duration)
            < datetime.now()
        ):  # the session has expired
            return None

        return session.get("user_id")
