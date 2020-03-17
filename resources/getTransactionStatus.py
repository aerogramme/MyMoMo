from flask import jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.config import mongo


# def argParser():
#     parser = RequestParser(bundle_errors=True)
#     parser.add_argument("transactionid", type=str, required=True, help="Transaction ID is Required")
#     return parser

class GetTransactionStatus(Resource):
    def get(self,transaction_id):
        '''Check if Phone Number Exist in DB'''
        #args = argParser()
        #transaction_id = args.parse_args().get("transactionid")
        userAccount = mongo.db.Transfer.find_one({"TransactionID": transaction_id})

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
