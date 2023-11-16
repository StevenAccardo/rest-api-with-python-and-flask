from db import db


class TagModel(db.Model):
    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), nullable=False)
    # Many-to-one
    store = db.relationship("StoreModel", back_populates="tags")
    # Many-to-many
    # Secondary argument tells sqlalchemy to refence the secondary table to work with the many-to-many relationship. SQLAlchemy will take the id of the current tag object, and use the secondary table to find the items related to that tag id.
    items = db.relationship("ItemModel", back_populates="tags", secondary="items_tags")