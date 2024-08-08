#!/usr/bin/env python3
""" DocDocDocDocDocDoc
"""
from flask import Blueprint
from models.user import User
from api.v1.views.session_auth import session_auth
from api.v1.views.index import *
from api.v1.views.users import *

# Create a Blueprint for the API
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Register the session_auth blueprint
app_views.register_blueprint(session_auth)

User.load_from_file()
