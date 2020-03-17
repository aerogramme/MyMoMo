from flask import jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.config import mongo


# def argParser():
#     parser = RequestParser(bundle_errors=True)
#     parser.add_argument("phone", type=str, required=True, help="Phone Number Required : format -> 0243559227")
#     return parser

class AccountVerification(Resource):
    def get(self, phone_number):
        '''Check if Phone Number Exist in DB'''
        #args = argParser()
        #phone_number = args.parse_args().get("phone")
        userAccount = mongo.db.Register({"Phone": phone_number})

        print(userAccount)

        if userAccount.count_documents({"Phone": phone_number}) > 0:
            jsonResonpse = {
                "code": 200,
                "status": "SUCCESS",
                "message": {
                "registration_status": "Registered",
                "registered_name": userAccount["firstname"] + " " + userAccount["lastname"]
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
