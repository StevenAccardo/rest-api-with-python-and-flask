# rest-api-with-python-and-flask

## Stack Used

A REST API that allows users to create stores, items, and tag items. The API consistes of user related endpoints that allow register, login, logout, refresh tokens. There are store, item, and tag endpoints that allow CRUD operations for each of the objects. This currently uses an SQLlite database, but can easily be shifted to use a PostgreSQL database. There are models created using SQLalchemy as well as schemas to be used with marshmallow for marshalling request/response shapes. Swagger documentation is also set up with some minimal error handling/responses.

This is a development only example would need increased functionality, relationships, and documentation to be production ready. It's just for funsies and practice.

1. python
2. flask
3. flask-smorest
4. sqlalchemy
5. flask-jwt-extended
6. passlib
7. docker
