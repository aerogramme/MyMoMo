from flask import jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.config import mongo
from common.auth import verify_password, users, unauthorized, auth

# make sure to retrieve data from database
verify_password(users.get("username"), users.get("password"))
unauthorized

# def argParser():
#     parser = RequestParser(bundle_errors=True)
#     parser.add_argument("phone", type=str, required=True, help="Phone Number Required : format -> 0243559227")
#     return parser

class AccountVerification(Resource):
    @auth.login_required
    def get(self, phone):
        '''Check if Phone Number Exist in DB'''
        #args = argParser()
        #phone_number = args.parse_args().get("phone")
        userAccount = mongo.db.Register.find_one({"Phone": phone})

        if userAccount:
            jsonResonpse = {
                "code": 200,
                "status": "SUCCESS",
                "response": {
                "registration_status": "Registered",
                "registered_name": userAccount["FirstName"]+" "+userAccount["LastName"]
                }
            }
            return jsonify(jsonResonpse)
        else:
            jsonResonpse = {
                "code": 403,
                "status":"FAILED",
                "response": {
                "registration_status": "No action required, Mobile number is not registered to receive transaction.",
                "registered_name": "Unknown"
                }
            }
            return jsonify(jsonResonpse)
