from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from app.models import Trail, Feature

class FeatureSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Feature
        load_instance = True
    
    TrailFeatureID = fields.Integer(dump_only=True)
    TrailFeature = fields.String(required=True)

class TrailSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Trail
        load_instance = True
        include_fk = True

    TrailID = fields.Integer(dump_only=True)

    # Nest the features
    features = fields.Nested(FeatureSchema, many=True, dump_only=True)
