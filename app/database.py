from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from app.config import Config

db = SQLAlchemy()
db_session = None

def init_db(app):
    global db_session

    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_ECHO'] = Config.SQLALCHEMY_ECHO
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS

    db.init_app(app)

    with app.app_context():
        db.create_all()

    engine = create_engine(Config.SQLALCHEMY_DATABASE_URI, echo=Config.SQLALCHEMY_ECHO)
    session_factory = sessionmaker(bind=engine)
    db_session = scoped_session(session_factory)

