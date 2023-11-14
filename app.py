import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

from blocklist import BLOCKLIST
from db import db
from resources.store import blp as StoreBlueprint
from resources.item import blp as ItemBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):
    # Loads env vars from .env file
    load_dotenv()
    # Instantiates our flask application
    app = Flask(__name__)

    # Tells flask to bubble any errors/exceptions in any extensions of flask up to the main app so that we can be notified of them.
    app.config["PROPAGATE_EXCEPTIONS"] = True
    # Names the application
    app.config["API_TITLE"] = "Store REST API"
    # The version of our API
    app.config["API_VERSION"] = "v1"
    # Tells flask-smorest which version of open API to use
    app.config["OPENAPI_VERSION"] = "3.0.3"
    # Tells flask-smorest where the root of the API is.
    app.config["OPENAPI_URL_PREFIX"] = "/"
    # Tells flask-smorest where to render the swagger ui.
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    # Tells flask-smorest where to download the swagger library from for documenting our API.
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    # Sets the database URI to be used with SQLAlchemy. This is part of the flask-sqlalchemy configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URI", "sqlite:///data.db")
    # Allows tracking of db queries. Adds significant overhead. Disabled by default in flask-sqlalchemy v3
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    # Initializes the application using flask-sqlalchemy
    db.init_app(app)

    # Connects flask-smorest with our flask app to help build out REST APIs
    api = Api(app)

    # Configures the flask-jwt-extended extension to user our secret when encoding and decoding JWTs
    app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')

    # Registers the JWTManager instance with our flask application
    jwt = JWTManager(app)

    # Checks whether the jti, or JWT ID, has been placed in the blocklist to determine if the JWT has been revoked, or not.
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST


    # Executed if a revoked token is encountered, if the @jwt.token_in_blocklist_loader callback returns True
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401,
        )

    # Executed if an expired token is encountered
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    # Executed if the token was unable to be verified
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    # Executed when request to a protected route does not have an access token
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    
    # Executed when a fresh token is required for a route, but the token provided is not fresh
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    # Creates the database tables that are missing from the database.
    with app.app_context():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app