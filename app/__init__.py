import connexion
from flask import Flask
from app.database import init_db
from app.config import Config

def create_app():
    connex_app = connexion.FlaskApp(__name__, specification_dir='.')
    app = connex_app.app
    app.config.from_object(Config)

    # Initialize the database
    init_db(app)

    # Add the API specification
    connex_app.add_api('../app.yaml', strict_validation=True, validate_responses=True)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        from app.database import db_session
        db_session.remove()

    return connex_app


# Typically you'd run from here if directly (python -m app)
if __name__ == '__main__':
    connex_app = create_app()
    connex_app.run(host='0.0.0.0', port=5000, debug=True)
