from flask import request, jsonify
from app.database import db_session
from app.models import Trail, User
from app.schemas import TrailSchema
import requests
from app.config import Config

trail_schema = TrailSchema()
trails_schema = TrailSchema(many=True)


def authenticate_user(email, password):
    """
    Authenticate the user against the Authenticator API and fetch role.
    """
    try:
        response = requests.post(
            Config.AUTH_API_URL,
            headers={"Content-Type": "application/json"},
            json={"email": email, "password": password}
        )
        if response.status_code == 200 and response.json() == ["Verified", "True"]:
            with db_session() as session:
                user = session.query(User).filter_by(Email_address=email).first()  
                if user:
                    return {"authenticated": True, "role": user.Role, "user_id": user.UserID}
                else:
                    return {"authenticated": False}  # Handle case where user is not found
        else:
            return {"authenticated": False}
    except requests.RequestException as e:
        print(f"Authentication API error: {e}")
        return {"authenticated": False}



def get_trails():
    """
    GET /trails - Admins see all trails, users see only their trails.
    """
    email = request.headers.get("email")
    password = request.headers.get("password")

    auth_result = authenticate_user(email, password)
    if not auth_result["authenticated"]:
        return jsonify({"error": "Unauthorized"}), 401

    with db_session() as session:
        if auth_result["role"] == "admin":
            trails = session.query(Trail).all()
        else:
            trails = session.query(Trail).filter_by(OwnerID=auth_result["user_id"]).all()
        return jsonify(trails_schema.dump(trails)), 200


def create_trail():
    """
    POST /trails - Users can create trails owned by them.
    """
    email = request.headers.get("email")
    password = request.headers.get("password")

    auth_result = authenticate_user(email, password)
    if not auth_result["authenticated"]:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    data["OwnerID"] = auth_result["user_id"]  # Set the owner ID to the authenticated user.

    with db_session() as session:
        new_trail = trail_schema.load(data, session=session)
        session.add(new_trail)
        session.commit()
        return jsonify(trail_schema.dump(new_trail)), 201


def get_trail(trail_id):
    """
    GET /trails/{trail_id} - Admins can access any trail, users only their own.
    """
    email = request.headers.get("email")
    password = request.headers.get("password")

    auth_result = authenticate_user(email, password)
    if not auth_result["authenticated"]:
        return jsonify({"error": "Unauthorized"}), 401

    with db_session() as session:
        trail = session.query(Trail).get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        if auth_result["role"] != "admin" and trail.OwnerID != auth_result["user_id"]:
            return jsonify({"error": "Forbidden"}), 403

        return jsonify(trail_schema.dump(trail)), 200


def update_trail(trail_id):
    """
    PUT /trails/{trail_id} - Admins can update any trail, users only their own.
    """
    email = request.headers.get("email")
    password = request.headers.get("password")

    auth_result = authenticate_user(email, password)
    if not auth_result["authenticated"]:
        return jsonify({"error": "Unauthorized"}), 401

    with db_session() as session:
        trail = session.query(Trail).get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        if auth_result["role"] != "admin" and trail.OwnerID != auth_result["user_id"]:
            return jsonify({"error": "Forbidden"}), 403

        data = request.get_json()
        for key, value in data.items():
            setattr(trail, key, value)
        session.commit()
        return jsonify(trail_schema.dump(trail)), 200


def delete_trail(trail_id):
    """
    DELETE /trails/{trail_id} - Admins can delete any trail, users only their own.
    """
    email = request.headers.get("email")
    password = request.headers.get("password")

    auth_result = authenticate_user(email, password)
    if not auth_result["authenticated"]:
        return jsonify({"error": "Unauthorized"}), 401

    with db_session() as session:
        trail = session.query(Trail).get(trail_id)
        if not trail:
            return jsonify({"error": "Trail not found"}), 404

        if auth_result["role"] != "admin" and trail.OwnerID != auth_result["user_id"]:
            return jsonify({"error": "Forbidden"}), 403

        session.delete(trail)
        session.commit()
        return '', 204
