from werkzeug.security import generate_password_hash, check_password_hash

from app.database import db

class Trail(db.Model):
    __tablename__ = 'TRAIL'
    __table_args__ = {'schema': 'CW2'} 

    TrailID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailName = db.Column(db.String(100), nullable=False)
    TrailSummary = db.Column(db.String(255))
    TrailDescription = db.Column(db.String(1000))
    Difficulty = db.Column(db.String(50))
    Location = db.Column(db.String(100))
    Length = db.Column(db.Numeric(10,2))
    ElevationGain = db.Column(db.Numeric(10,2))
    RouteType = db.Column(db.String(50))
    OwnerID = db.Column(db.Integer, db.ForeignKey('CW2.USER.UserID'))
    Pt1_Lat = db.Column(db.Numeric(9,6))
    Pt1_Long = db.Column(db.Numeric(9,6))
    Pt1_Desc = db.Column(db.String(255))
    Pt2_Lat = db.Column(db.Numeric(9,6))
    Pt2_Long = db.Column(db.Numeric(9,6))
    Pt2_Desc = db.Column(db.String(255))

    features = db.relationship(
        'Feature',
        secondary='CW2.TRAILFEATURE',  
        back_populates='trails'
    )

    owner = db.relationship('User', back_populates='trails')

class User(db.Model):
    __tablename__ = 'USER'
    __table_args__ = {'schema': 'CW2'}

    UserID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Email_address = db.Column(db.String(255), nullable=False, unique=True)
    Role = db.Column(db.String(50), nullable=False)
    PasswordHash = db.Column(db.String(255), nullable=False)

    def set_password(self, password):
        """Hashes a plaintext password and stores it."""
        self.PasswordHash = generate_password_hash(password)

    def check_password(self, password):
        """Checks the hashed password against a plaintext password."""
        return check_password_hash(self.PasswordHash, password)

    trails = db.relationship('Trail', back_populates='owner')

class Feature(db.Model):
    __tablename__ = 'FEATURE'
    __table_args__ = {'schema': 'CW2'}

    TrailFeatureID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    TrailFeature = db.Column(db.String(255), nullable=False)

    trails = db.relationship(
        'Trail',
        secondary='CW2.TRAILFEATURE',
        back_populates='features'
    )

class TrailFeature(db.Model):
    __tablename__ = 'TRAILFEATURE'
    __table_args__ = {'schema': 'CW2'}

    TrailID = db.Column(db.Integer, db.ForeignKey('CW2.TRAIL.TrailID'), primary_key=True)
    TrailFeatureID = db.Column(db.Integer, db.ForeignKey('CW2.FEATURE.TrailFeatureID'), primary_key=True)
