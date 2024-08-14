#!/usr/bin/env python3
"""Basic Flask app.
"""

from flask import Flask, request, jsonify, abort, make_response
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def welcome():
    """Return a JSON payload with a welcome message."""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    """Register a new user."""
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    """Login route to create a new session for the user.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = jsonify({"email": email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response

@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """Logout route to destroy a user's session.
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        return abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        return abort(403)

    AUTH.destroy_session(user_id)
    return redirect(url_for("welcome"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
