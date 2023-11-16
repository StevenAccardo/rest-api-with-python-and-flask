
from db import db

# Uses flask-sqlalchemy to create sub-classes from a SQLAlchemy declarative class exposed by using the db.Model pattern.
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)