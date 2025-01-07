# tests/test_models.py

from app.models import Trail, Feature, TrailFeature

def test_trail_model(db):
    """
    Tests that we can create a Trail in the DB, then query it.
    """
    # 1. Create
    new_trail = Trail(TrailName="Test Trail")
    db.session.add(new_trail)
    db.session.commit()

    # 2. Query
    saved = Trail.query.filter_by(TrailName="Test Trail").first()
    assert saved is not None
    assert saved.TrailName == "Test Trail"

def test_trail_feature_relationship(db):
    """
    Tests that we can associate a Feature with a Trail (many-to-many)
    and retrieve them through the relationship.
    """
    # 1. Create a Trail and a Feature
    t = Trail(TrailName="Trail with Feature")
    f = Feature(TrailFeature="Waterfall")
    db.session.add_all([t, f])
    db.session.commit()

    # 2. Associate
    t.features.append(f)
    db.session.commit()

    # 3. Refresh and check
    saved_trail = Trail.query.filter_by(TrailName="Trail with Feature").first()
    assert len(saved_trail.features) == 1
    assert saved_trail.features[0].TrailFeature == "Waterfall"
