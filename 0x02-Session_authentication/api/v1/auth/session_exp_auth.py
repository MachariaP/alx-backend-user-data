#!/usr/bin/env python3

"""This module defines a class for expiring sessions"""
import os
from datetime import datetime, timedelta
from typing import Union
import logging

from api.v1.auth.session_auth import SessionAuth

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class SessionExpAuth(SessionAuth):
    """Implement Session Expiry Authentication class."""

    def __init__(self):
        """Initialize the session expiration object."""
        super().__init__()
        try:
            self.session_duration = int(os.environ.get("SESSION_DURATION", 0))
        except ValueError:
            self.session_duration = 0
        logger.debug(f"Session duration set to {
                     self.session_duration} seconds")

    def create_session(self, user_id: str = None) -> Union[str, None]:
        """Create an expirable session."""
        session_id = super().create_session(user_id=user_id)
        if not session_id:
            return None

        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now(),
        }
        logger.debug(f"Session created for user_id {
                     user_id} with session_id {session_id}")

        return session_id

    def user_id_for_session_id(
        self, session_id: str = None
    ) -> Union[str, None]:
        """Return the User ID for the user who owns a given session ID."""
        if not session_id:
            return None

        session = self.user_id_by_session_id.get(session_id, {})

        if "created_at" not in session:
            logger.debug(f"Session ID {
                         session_id} does not have a creation time")
            return None

        if self.session_duration <= 0:  # non-expiry session
            return session.get("user_id")

        if (
            session.get("created_at")
            + timedelta(seconds=self.session_duration)
            < datetime.now()
        ):  # the session has expired
            logger.debug(f"Session ID {session_id} has expired")
            return None

        return session.get("user_id")
