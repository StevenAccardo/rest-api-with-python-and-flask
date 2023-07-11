import os

from flask import Flask
from flask_smorest import Api
from db import db
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint

def create_app(db_url=None):
    app = Flask(__name__)

    # Tells flask to bubble any errors/exceptions in any extensions of flask up to the main app so that we can be notified of them.
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    # Tells flask-smorest which version of open API to use
    app.config["OPENAPI_VERSION"] = "3.0.3"
    # Tells flask-smorest where the root of the API is.
    app.config["OPENAPI_URL_PREFIX"] = "/"
    # Tells flask-smorest where to render the swagger ui.
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # Tells flask-smorest where to download the swagger library from for documenting our API.
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URI", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    db.init_app(app)

    # Connects flask-smorest with our flask app
    api = Api(app)

    with app.app_context():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)

    return app