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
#     parser.add_argument("transactionid", type=str, required=True, help="Transaction ID is Required")
#     return parser

class GetTransactionStatus(Resource):
    @auth.login_required
    def get(self,transaction_id):
        '''Check if Phone Number Exist in DB'''
        #args = argParser()
        #transaction_id = args.parse_args().get("transactionid")
        userTransfer = mongo.db.Transfer.find_one({"TransactionID": transaction_id})
        userTopup = mongo.db.TopUps.find_one({"TransactionID": transaction_id})
        userWithdraw = mongo.db.Withdrawal.find_one({"TransactionID": transaction_id})

        if userTransfer is not None:
            jsonResonpse = {
                "code": 200,
                "status": userTransfer["Status"],
                "response": {
                    "ConfirmationNumber":userTransfer["ConfirmationNumber"],
                    "Amount": userTransfer["AmountBeforeFees"],
                    "TransactionID": userTransfer["TransactionID"],
                    "Phone": userTransfer["SenderPhone"],
                    "Created_At": userTransfer["Created_At"]
                }
            }
            return jsonify(jsonResonpse)
        elif userTopup is not None:
            jsonResonpse = {
                "code": 200,
                "status": userTopup["Status"],
                "response": {
                    "ConfirmationNumber":userTopup["ConfirmationNumber"],
                    "Amount": userTopup["Amount"],
                    "TransactionID": userTopup["TransactionID"],
                    "Phone": userTopup["SenderPhone"],
                    "CreatedAt": userTopup["CreatedAt"]
                }
            }
            return jsonify(jsonResonpse)
        elif userWithdraw is not None:
            jsonResonpse = {
                "code": 200,
                #"status": userWithdraw["Status"],
                "response": {
                    #"ConfirmationNumber":userWithdraw["ConfirmationNumber"],
                    "Amount": userWithdraw["Amount"],
                    "TransactionID": userWithdraw["TransactionID"],
                    "Phone": userWithdraw["Phone"],
                    "Created_At": userWithdraw["DateTime"]
                }
            }
            return jsonify(jsonResonpse)

        else:
            jsonResonpse = {
                "code": 403,
                "status":"FAILED",
                "response": {
                "registration_status": "No action required, Transaction ID :{} Not Found!".format(transaction_id),
                "registered_name": "Unknown"
                }
            }
            return jsonify(jsonResonpse)

