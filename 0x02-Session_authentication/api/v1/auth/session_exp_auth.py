import os
from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class that inherits from SessionAuth and\
            adds session expiration
    """

    def __init__(self):
        """
        Initialize the SessionExpAuth instance.
        Sets session duration from the environment variable SESSION_DURATION.
        If environment variable is not set or cannot be parsed, defaults to 0.
        """
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', 0))
        except valueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create and store the session details with an expiration time.

        Args:
            user_id (str): The user ID for which the session is being created.

        Return:
            str: The session ID created, or None if creation failed.
        """
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        session_dict = {
                'user_id': user_id,
                'created_at': datetime.now()
                }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrive the user ID associated with a session ID,\
                considering session expiration.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str: The user ID if the session is valid, or\
                    None if the session is invalid.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if not session_dict:
            return None
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if not created_at:
            return None
        if created_at + timedelta(
                seconds=self.session_duration) < datetime.now():
            return None
        return session_dict.get('user_id')
