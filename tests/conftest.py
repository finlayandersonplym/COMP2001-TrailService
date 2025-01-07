import pytest
from app import create_app
from app.database import db as _db
from app.config import Config
from app.models import User
from werkzeug.security import generate_password_hash

@pytest.fixture
def app():
    """
    Create a new Flask app instance for testing.
    """
    connex_app = create_app()
    app = connex_app.app

    with app.app_context():
        yield app

        
@pytest.fixture(scope="function")
def default_user(db):
    # Create a default user with UserID=1
    user = User(UserID=1, Email_address="user@example.com", Role="user")
    user.set_password("test_password")
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def client(app):
    """
    Returns a test client for the app.
    """
    return app.test_client()

@pytest.fixture
def db(app):
    """
    Creates a fresh database (schema) before each test, 
    then drops it afterward.
    """
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()
