from flask import jsonify, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

users = {
    "freeworldboss": generate_password_hash("$5$rounds=535000$gUf/KanM4MwLtl1d$Ay93DrMK0JJRdROIddzXoNOJN12.8YtwvEvkvarM2wC"),
    "Kartel": generate_password_hash("bye")
}

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'Error': 'Unauthorized Access'}), 401)
