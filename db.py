from flask_sqlalchemy import SQLAlchemy

# Using flask-asqlalchemy library to create the database instance which bootstraps some of the manual process of creating it that we would have to do if using SQLAlchemy directly.
db = SQLAlchemy()