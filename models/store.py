from db import db

class StoreModel(db.Model):
    __tablename__ = "stores"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    # Using the back_populates argument defines the other end of the relationship setup in the ItemModel. In this case there is no foreign key because this is a one to many relationship, with the store being the parent to the child items.
    # Using lazy=dynamic tells sqlalchemy not to preload the relations on any store queries until we request them
    # Cascade means that if you delete a store from the DB, the child or related items will be deleted as well.
    items = db.relationship("ItemModel", back_populates="store", lazy="dynamic", cascade="all, delete")
    # One-to-many
    tags = db.relationship("TagModel", back_populates="store", lazy="dynamic")