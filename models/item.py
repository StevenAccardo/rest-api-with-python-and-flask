from db import db

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    price = db.Column(db.Float(precision=2), unique=False, nullable=False)
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"), unique=False, nullable=False)
    # flask-sqlalchemy uses the store_id that we noted was a foreign key to populate the store object/row from the database that has that store_id
    # The back_populates argument then allows a store object to reference all of it's items.
    store = db.relationship("StoreModel", back_populates="items")
    # many-to-many
    # Secondary argument tells sqlalchemy to refence the secondary table to work with the many-to-many relationship. SQLAlchemy will take the id of the current item object, and use the secondary table to find the tags related to that tag id.
    tags = db.relationship("TagModel", back_populates="items", secondary="items_tags")