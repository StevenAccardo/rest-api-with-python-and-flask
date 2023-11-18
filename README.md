# rest-api-with-python-and-flask

## A REST API that allows users to create stores, items, and tag items belonging to that store. The API consists of user-related endpoints that allow register, login, logout, refresh tokens. There are store, item, and tag endpoints that allow CRUD operations for each of the objects. This currently uses an SQLite database, but can easily be shifted to use a PostgreSQL database. There are models created using SQLAlchemy as well as schemas to be used with marshmallow for marshalling request/response shapes. Swagger documentation is also set up with some minimal error handling/responses.

### This portfolio piece shows general programming, containerization, and deployment. So it is not a completely polished piece.

### You can reach swagger docs at {baseURL}/swaggger-ui

### Postman collection can be be found in ./postman directory.

#### Tech Stack Used:

- python
- flask
- flask-smorest
- SQLite
- sqlalchemy
- flask-sqlalchemy
- flask-jwt-extended
- passlib
- flask-cors
- docker
- gunicorn

#### Acknowleded Improvement Possibilities

Since this is a portfolio piece, there is room for improvement in making this truly production-level. I'll list some of them below so that you know I understand them.

1. UI - I've chosen to focus on backend projects at this time, but the Postman collection is there if you would like to interact with the server.
1. CORS - Right now I am letting any request in. I would want to limit this to the domain of the client if this were going to be loosely coupled with a frontend.
1. Auth - This is a basic auth flow. It doesn't include forgot password, change password, and etc. Ideally, I would leverage more robust auth libraries or services for something more critical.
1. Database - Right now this is using SQLite, and it would be better to connect it to a different database.
1. JWT Blocklist - Currently this is using a simple set which will lose the blocklist on any application restart and cannot share the blocklist across instances. A better solution would be to leverage key-value permenant storage such as Redis, or etc.
1. Pagination - Pagination could be added to return only a selection of items from the store
1. Unit testing
1. CI/CD and different branches/envs - I'm keeping everything on the main branch directly as I'm the only developer working on this.
