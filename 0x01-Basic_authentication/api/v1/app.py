#!/usr/bin/env python3
"""
Route module for the API.
"""
import os
from os import getenv
from flask import Flask, jsonify, abort, request, Response
from flask_cors import (CORS, cross_origin)
from api.v1.views import app_views
from api.v1.auth.auth import Auth
from typing import Tuple

app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

# Initialize the authentication variable
auth = None
auth_type = getenv('AUTH_TYPE', 'auth')
if auth_type == 'auth':
    auth = Auth()
elif auth_type == 'basic_auth':
    auth = BasicAuth()

@app.errorhandler(404)
def not_found(error) -> Tuple[Response, int]:
    """Not found handler."""
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(401)
def unauthorized(error) -> Tuple[Response, int]:
    """Unauthorized handler."""
    return jsonify({"error": "Unauthorized"}), 401

@app.errorhandler(403)
def forbidden(error) -> Tuple[Response, int]:
    """Forbidden handler."""
    return jsonify({"error": "Forbidden"}), 403

@app.before_request
def authenticate_user():
    """Authenticates a user before processing a request."""
    if auth:
        excluded_paths = [
            '/api/v1/status/',
            '/api/v1/unauthorized/',
            '/api/v1/forbidden/',
        ]
        if auth.require_auth(request.path, excluded_paths):
            auth_header = auth.authorization_header(request)
            user = auth.current_user(request)
            if auth_header is None:
                abort(401)
            if user is None:
                abort(403)

@app.route('/api/v1/status', methods=['GET'])
@app.route('/api/v1/status/', methods=['GET'])
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
