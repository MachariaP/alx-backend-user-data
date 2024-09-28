#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from typing import Dict, Tuple
import logging

from flask import Flask, abort, jsonify, request
from flask_cors import CORS

from api.v1.views import app_views

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None

auth_type = getenv("AUTH_TYPE")

if auth_type == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth

    auth = BasicAuth()
elif auth_type == "auth":
    from api.v1.auth.auth import Auth

    auth = Auth()
elif auth_type == "session_auth":
    from api.v1.auth.session_auth import SessionAuth

    auth = SessionAuth()
elif auth_type == "session_exp_auth":
    from api.v1.auth.session_exp_auth import SessionExpAuth

    auth = SessionExpAuth()
elif auth_type == "session_db_auth":
    from api.v1.auth.session_db_auth import SessionDBAuth

    auth = SessionDBAuth()


@app.errorhandler(404)
def not_found(_) -> Tuple[Dict, int]:
    """Not found handler"""
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(_) -> Tuple[Dict, int]:
    """Unauthorized error handler."""
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(_) -> Tuple[Dict, int]:
    """Forbidden API operation handler."""
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def auth_middleware():
    """Before request handler."""
    if auth is None:
        return None

    excluded_paths = [
        "/api/v1/status/",
        "/api/v1/unauthorized/",
        "/api/v1/forbidden/",
        "/api/v1/auth_session/login/",
    ]

    if not auth.require_auth(request.path, excluded_paths):
        return None

    auth_header = auth.authorization_header(request)
    session_cookie = auth.session_cookie(request)

    if auth_header and session_cookie:  # one auth type at a time.
        return None

    if not auth_header and not session_cookie:  # no auth type provided.
        abort(401)

    user = auth.current_user(request)
    if user is None:
        abort(403)

    request.current_user = user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=getenv("DEBUG", False))
