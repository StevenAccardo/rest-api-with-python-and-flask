from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required
from sqlalchemy.exc import SQLAlchemyError

from db import db
from models import ItemModel
from schemas import ItemSchema, ItemUpdateSchema

blp = Blueprint("Items", __name__, description="Operations on items.")

@blp.route("/item/<int:item_id>")
class Item(MethodView):
    @jwt_required()
    # Uses the schema to define/shape the main response JSON. If a returned property is not included in the schema, then it will be removed from the response JSON returned to the client.
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        # We can leverage this method due to using the flask-SQLalchemy library instead of just the SQLalchemy library. This uses the ItemObject's id to query the record and returns 404 if not found.
        return ItemModel.query.get_or_404(item_id)

    @jwt_required(fresh=True)
    def delete(self, item_id):
        item = ItemModel.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return {"message": "Item deleted."}

    @jwt_required(fresh=True)

    # Uses the schema to define/validate request JSON, and then passess that validated JSON as a dictionary to the method as the 2nd argument.
    @blp.arguments(ItemUpdateSchema)
    # Uses the schema to define/shape the main response JSON. If a returned property is not included in the schema, then it will be removed from the response JSON returned to the client.
    @blp.response(200, ItemSchema)
    def put(self, item_data, item_id):
        item = ItemModel.query.get(item_id)
        if item:
            item.price = item_data["price"]
            item.name = item_data["name"]
        else:
            item = ItemModel(id=item_id, **item_data)
        
        db.session.add(item)
        db.session.commit()

        return item


@blp.route("/item")
class ItemList(MethodView):
    @jwt_required()
    # Uses the schema to define/shape the main response JSON. If a returned property is not included in the schema, then it will be removed from the response JSON returned to the client.
    # many=True as an argument to the instance of the subclass directs flask-smorest that an array of the schema type will be sent in the response
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()
    
    @jwt_required(fresh=True)
    # Uses the schema to define/validate request JSON, and then passess that validated JSON as a dictionary to the method as the 2nd argument.
    @blp.arguments(ItemSchema)
    # Uses the schema to define/shape the main response JSON. If a returned property is not included in the schema, then it will be removed from the response JSON returned to the client.
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occured while inserting the item.")
        return item