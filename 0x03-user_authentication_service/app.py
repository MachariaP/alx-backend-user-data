#!/usr/bin/env python3
"""Basic Flask app.
"""

from flask import Flask, request, jsonify, abort, make_response
from flask import redirect, url_for
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
    print(f"Session ID: {session_id}")

    if session_id is None:
        print("No session ID found, aborting with 403")
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)
    print(f"User: {user}")

    if user is None:
        print("No user found for session ID, aborting with 403")
        abort(403)

    try:
        AUTH.destroy_session(user.id)
        print("Session destroyed")
    except Exception as e:
        print(f"Error destroying session: {e}")
        abort(500)

    try:
        response = make_response(jsonify({"message": "Bienvenue"}))
        response.set_cookie("session_id", '', expires=0)
        response.status_code = 200
        print(f"Response status code: {response.status_code}")
    except Exception as e:
        print(f"Error creating response: {e}")
        abort(500)

    return response


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """Profile route to get the user's profile information.
    """
    session_id = request.cookies.get("session_id")

    if session_id is None:
        abort(403)

    user = AUTH.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    """Generate a password reset token for the user identified by theemail.
    """
    email = request.form.get("email")

    if not email:
        abort(400, description="Email is required")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        return jsonify({"message": "email not found"}), 403


@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password() -> str:
    """Update the user's password using the reset token.
    """
    email = request.form.get("email")
    reset_token = request.form.get("password")
    new_password = request.form.get("new_password")

    if not email or not reset_token or not new_password:
        abort(400, description=(
            "Email, reset token and new password are required"
            ))

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError:
        return jsonify({"message": "Invalid reset token"}), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
