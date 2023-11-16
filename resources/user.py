from flask.views import MethodView
from flask_smorest import Blueprint, abort
# Imports a specific hashing algorithm
from passlib.hash import pbkdf2_sha256
# get_jwt_identity is a helper function for getting the decoded jwt sub property where the user id is stored. Similar to get_jwt().get('sub').
from flask_jwt_extended import create_access_token, create_refresh_token, get_jwt_identity, get_jwt, jwt_required

from db import db
from models import UserModel
from schemas import UserSchema
from blocklist import BLOCKLIST


blp = Blueprint("Users", __name__, description="Operations on users")

# Register's a user and inserts their data into the database
@blp.route("/register")
class UserRegister(MethodView):
    
    # Uses the schema to define/validate request JSON, and then passess that validated JSON as a dictionary to the method as the 2nd argument.
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # Query the table to see if the incoming request username matches one already stored.
        if UserModel.query.filter(UserModel.username == user_data["username"]).first():
            abort(409, message="A user with that username already exists.")

        user = UserModel(
            username=user_data["username"],
            # This method will generate a random salt, selects default hashing rounds, and hashes the plain text + salt combination
            # Since the salt is random, the salting + hashing of the same plain text password would result in different returned hashes.
            password=pbkdf2_sha256.hash(user_data["password"])
        )
        # Inserts new user into the table and commits the transaction to the database.
        db.session.add(user)
        db.session.commit()

        return {"message": "User created successfully."}, 201
    
    # Checks the user request info against the database, returning an access_token and refresh_token if the user info is found and matches.
    @blp.route("/login")
    class UserLogin(MethodView):

        # Uses the schema to define/validate request JSON, and then passess that validated JSON as a dictionary to the method as the 2nd argument.
        @blp.arguments(UserSchema)
        def post(self, user_data):
            # Queries user table for the username
            user = UserModel.query.filter(
                UserModel.username == user_data["username"]
            ).first()

            # If username was found, and password hashes are equal, return the access token.
            if user and pbkdf2_sha256.verify(user_data["password"], user.password):
                # Sets a fresh=True claim on the JWT since this was returned due to a login request.
                access_token = create_access_token(identity=user.id, fresh=True)
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200

            abort(401, message="Invalid credentials.")

    # Adds the JWT jti to the blocklist disallowing any further requests to protected endpoints using that JWT
    @blp.route("/logout")
    class UserLogout(MethodView):
        @jwt_required()
        def post(self):
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            return {"message": "Successfully logged out"}, 200

    # This request can be made to retrieve a new, non-fresh token to allow the user to continue using the API without excplicitly having to login again.
    # The non-fresh token will limit their ability to certain api endpoint functionalities.
    @blp.route("/refresh")
    class TokenRefresh(MethodView):
        #Only accepts the refresh token.
        @jwt_required(refresh=True)
        def post(self):
            # Retrieve the user id off of the sub property
            current_user = get_jwt_identity()
            # Set fresh to false
            new_token = create_access_token(identity=current_user, fresh=False)
            # If you want to only allow one refresh token use, then you can add the refresh token to the block list. Then if the client tried to use it again to get another non-fresh access token, they would be denied. Forcing the client to login again to get a new fresh access token and another refresh token.
            jti = get_jwt()["jti"]
            BLOCKLIST.add(jti)
            return {"access_token": new_token}, 200
    

# @blp.route("/user/<int:user_id>")
# class User(MethodView):
#     """
#     This resource can be useful when testing our Flask app.
#     """
#     # Uses the schema to define/shape the main response JSON. If a returned property is not included in the schema, then it will be removed from the response JSON returned to the client.
#     def get(self, user_id):
#         user = UserModel.query.get_or_404(user_id)
#         return user

#     def delete(self, user_id):
#         user = UserModel.query.get_or_404(user_id)
#         db.session.delete(user)
#         db.session.commit()
#         return {"message": "User deleted."}, 200