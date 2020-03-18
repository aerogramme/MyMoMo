# WITHDRAW MONEY
from flask import request, jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.auth import verify_password, users, unauthorized, auth
from common.config import mongo
from common.utils import getNetworkName, verifyCredentials, cashWithUser, updateAccount, transaction_id, date_time, \
    generateReturnDictionary,withdraw_confirmation_number

# make sure to retrieve data from database
verify_password(users.get("username"), users.get("password"))
unauthorized


def argParser():
    parser = RequestParser(bundle_errors=True)
    parser.add_argument("fromPhone", type=str, required=True, help="Phone Number Required:format -> 0243559227")
    parser.add_argument("amount", type=float, required=True, help="Amount Required")
    parser.add_argument("vendorid", type=str, required=False, help="Vendor ID Required")
    return parser

class WithdrawCash(Resource):
    @auth.login_required
    def post(self):

        args = argParser()
        phone = args.parse_args().get("fromPhone")
        amount = args.parse_args().get("amount")
        vendorId = args.parse_args().get("vendorid")
        network = getNetworkName(phone)

        try:
            # Current Balance
            balance = cashWithUser(phone)

            if balance < amount:
                return jsonify(generateReturnDictionary(303, "Not Enough Cash in your mobile wallet", "FAILURE"))
            elif amount <= float(0):
                return jsonify(generateReturnDictionary(303, "You cannot withdraw negative amount", "FAILURE"))
            elif balance < float(0):
                return jsonify(
                    generateReturnDictionary(303, "Your balance is in negative, please add some cash", "FAILURE"))

            # deduct money from vendor or customer
            updateAccount(phone, balance - amount)

            trans_id = transaction_id()
            withdraw_number = withdraw_confirmation_number()

            # Insert data into Withdrawal Collection
            mongo.db.Withdrawal.insert_one({
                #"AmountBeforeFees": round(float(amount), 2),
                #"AmountAfterFees": round(float(amount_after), 2),
                "Amount": round(float(amount), 2),
                "Network": network,
                "Phone": phone,
                "VendorID": vendorId,
                "TransactionID": trans_id,
                "ConfirmationNumber": withdraw_number,
                "CreatedAt": date_time(),
                "Status":"SUCCESS"
            })
            jResponse = {
                "code": 200,
                "status": "SUCCESS",
                "amount": float(amount),
                "transaction_ID":trans_id,
                "confirmation_Number": withdraw_number,
                "message": "Money withdrawn successfully from your wallet",
                "response": "Transaction was successful"
             }
            return jsonify(jResponse)

        except Exception as e:
            retJson = {
                "code": 409,
                "message": "There was an error while trying to withdraw money from your wallet -> , try again!",
                "status": "FAILURE: {0}".format(e.message)
            }
            return jsonify(retJson)


