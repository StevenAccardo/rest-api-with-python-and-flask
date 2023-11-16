from flask import request

# Routes incoming requests to the methods that are defined on the subclasses within this module.
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from db import db
from models import StoreModel
from schemas import StoreSchema


blp = Blueprint("Stores", __name__, description="Operations on stores.")

# @blp.route connects flask-smorest with the flask methodview subclass, so that when we make a request to the endpoint it is set to the appropriate endpoint
@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @jwt_required()
    # Uses the schema to define/shape the main response JSON. If a returned property is not included in the schema, then it will be removed from the response JSON returned to the client.
    @blp.response(200, StoreSchema)
    def get(self, store_id):
        return StoreModel.query.get_or_404(store_id)

    @jwt_required(fresh=True)
    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        # Deleting a store will cascade delete all the children items owned by that store as well because we set the database up to do this through our store model.
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted."}

# @blp.route connects flask-smorest with the flask methodview subclass, so that when we make a request to the endpoint it is set to the appropriate endpoint
@blp.route("/store")
class StoreList(MethodView):
    @jwt_required()
    # Uses the schema to define/shape the main response JSON. If a returned property is not included in the schema, then it will be removed from the response JSON returned to the client.
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        return StoreModel.query.all()
       
    @jwt_required(fresh=True)
    # Uses the schema to define/validate request JSON, and then passess that validated JSON as a dictionary to the method as the 2nd argument.
    @blp.arguments(StoreSchema)
    # Uses the schema to define/shape the main response JSON. If a returned property is not included in the schema, then it will be removed from the response JSON returned to the client.
    @blp.response(201, StoreSchema)
    def post(self, store_data):
        # Using the ** allows us to separate the passed in dictionary into keyword arguments. The keys must exactly match what the properties that the model is expecting.
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        # This error is thrown when our add violates the constraints set on the table.
        except IntegrityError:
             abort(400, message="A store with that name already exists.")
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")

        return store