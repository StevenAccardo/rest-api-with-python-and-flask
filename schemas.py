# Marshmallow is a dependency of flask-smorest, so we get access to it without directly having to add it to the requirements.txt
from marshmallow import Schema, fields

# The schemas that will be used by flask-smorest to define our api swagger documentation as well as validate our requests and responses.
# "Plain" schemas are meant to exclude relationships for cases where we want to accept or return only a db object without its relationship objects/data. These also help us avoid recursive issues when we are using nesting.
class PlainItemSchema(Schema):
    # dump_only for response properties
    id = fields.Int(dump_only=True)
    # required= True means that the property must be present on both the request and the response JSON
    name = fields.Str(required=True)
    price = fields.Float(required=True)

class PlainStoreSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class PlainTagSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str()

# "Non-plain" schemas include relationship objects
# Inherits from the "plain" schema to get all of its properties, and then adds additional properties
class ItemSchema(PlainItemSchema):
    # load_only=True means that the property is only required on the request
    store_id = fields.Int(required=True, load_only=True)
    # Nested class is used for related objects/rows 
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()
    store_id = fields.Int()

class StoreSchema(PlainStoreSchema):
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    tags = fields.List(fields.Nested(PlainTagSchema()), dump_only=True)

class TagSchema(PlainTagSchema):
    store_id = fields.Int(load_only=True)
    store = fields.Nested(PlainStoreSchema(), dump_only=True)
    items = fields.List(fields.Nested(PlainItemSchema()), dump_only=True)
    
class TagAndItemSchema(Schema):
    message = fields.Str()
    item = fields.Nested(ItemSchema)
    tag = fields.Nested(TagSchema)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)