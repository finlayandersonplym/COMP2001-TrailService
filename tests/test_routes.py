import json
import pytest
from unittest.mock import patch
from app.models import User

def get_auth_headers(email="user@example.com", password="password"):
    """
    Helper function to generate authentication headers for tests.
    """
    return {"email": email, "password": password}

@patch("app.routes.authenticate_user")

def test_get_empty_trails(mock_auth, client, db, default_user):
    """
    GET /trails when there are no trails in the DB.
    Should return 200 and an empty list.
    """
    mock_auth.return_value = {"authenticated": True, "role": "user", "user_id": 1}
    headers = get_auth_headers()
    response = client.get("/trails", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


@patch("app.routes.authenticate_user")
def test_create_trail(mock_auth, client, db, default_user):
    """
    POST /trails to create a trail, then verify it was created.
    """
    mock_auth.return_value = {"authenticated": True, "role": "user", "user_id": 1}
    headers = get_auth_headers()
    body = {
        "TrailName": "New Trail",
        "TrailSummary": "Just a test",
    }
    response = client.post("/trails", json=body, headers=headers)
    assert response.status_code == 201

    created = response.get_json()
    assert created["TrailName"] == "New Trail"


@patch("app.routes.authenticate_user")
def test_get_trails_with_data(mock_auth, client, db, default_user):
    """
    GET /trails after we've inserted a trail into the DB directly.
    """
    from app.models import Trail

    mock_auth.return_value = {"authenticated": True, "role": "user", "user_id": 1}
    headers = get_auth_headers()

    # Insert a trail directly via the db fixture
    t = Trail(TrailName="DB Inserted Trail", OwnerID=1)
    db.session.add(t)
    db.session.commit()

    response = client.get("/trails", headers=headers)
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 1
    assert data[0]["TrailName"] == "DB Inserted Trail"


@patch("app.routes.authenticate_user")
def test_get_single_trail(mock_auth, client, db, default_user):
    """
    Test GET /trails/{trail_id} with an existing trail.
    """
    from app.models import Trail

    mock_auth.return_value = {"authenticated": True, "role": "user", "user_id": 1}
    headers = get_auth_headers()

    # Insert a trail
    t = Trail(TrailName="Single Trail", OwnerID=1)
    db.session.add(t)
    db.session.commit()
    tid = t.TrailID

    # GET the trail
    response = client.get(f"/trails/{tid}", headers=headers)
    data = response.get_json()
    assert response.status_code == 200
    assert data["TrailName"] == "Single Trail"


@patch("app.routes.authenticate_user")
def test_update_trail(mock_auth, client, db, default_user):
    """
    PUT /trails/{trail_id} to update an existing trail.
    """
    from app.models import Trail

    mock_auth.return_value = {"authenticated": True, "role": "user", "user_id": 1}
    headers = get_auth_headers()

    # Insert a trail
    t = Trail(TrailName="Old Trail", OwnerID=1)
    db.session.add(t)
    db.session.commit()
    tid = t.TrailID

    # Update the trail
    response = client.put(f"/trails/{tid}", json={"TrailName": "New Name"}, headers=headers)
    assert response.status_code == 200
    updated = response.get_json()
    assert updated["TrailName"] == "New Name"


@patch("app.routes.authenticate_user")
def test_delete_trail(mock_auth, client, db, default_user):
    """
    DELETE /trails/{trail_id} to remove a trail.
    """
    from app.models import Trail

    mock_auth.return_value = {"authenticated": True, "role": "user", "user_id": 1}
    headers = get_auth_headers()

    # Insert a trail
    t = Trail(TrailName="To Delete", OwnerID=1)
    db.session.add(t)
    db.session.commit()
    tid = t.TrailID

    # Confirm trail exists
    existing = db.session.query(Trail).get(tid)
    assert existing is not None

    # Delete the trail
    response = client.delete(f"/trails/{tid}", headers=headers)
    assert response.status_code == 204

    # Confirm it's gone
    db.session.expire_all()  # Clear session cache to ensure fresh query
    remaining = db.session.query(Trail).get(tid)
    assert remaining is None
