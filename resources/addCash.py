from flask import request, jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.auth import verify_password, users, unauthorized, auth
from common.config import mongo
from common.utils import getNetworkName, verifyCredentials, cashWithUser, updateAccount, transaction_id, date_time, \
    generateReturnDictionary, transactionFee, addcash_confirmation_number

# make sure to retrieve data from database
verify_password(users.get("username"), users.get("password"))
unauthorized


def argParser():
    parser = RequestParser(bundle_errors=True)
    parser.add_argument("firstname", type=str, required=False, help="First Name Required")
    parser.add_argument("lastname", type=str, required=False, help="Last Name Required")
    parser.add_argument("fromPhone", type=str, required=True, help="Phone Number Required : format -> 0243559227")
    parser.add_argument("amount", type=float, required=True, help="Amount Required")
    parser.add_argument("description", type=str, required=False, help="Description of Transaction")
    parser.add_argument("email", type=str, required=False, help="Enter Email ID")
    parser.add_argument("service_type", type=str, required=False, help="Provide Service Type")
    return parser


class AddCash(Resource):
    @auth.login_required
    def post(self):
        # get json body
        args = argParser()
        firstname = args.parse_args().get("firstname")
        lastname = args.parse_args().get("lastname")
        phone = args.parse_args().get("fromPhone")
        amount = args.parse_args().get("amount")
        description = args.parse_args().get("description")
        email = args.parse_args().get("email")
        service_type = args.parse_args().get("service_type")
        network = getNetworkName(phone)

        # check if amount is not less than 0
        if amount <= float(0):
            return jsonify(generateReturnDictionary(304, "The amount entered must be greater than GHS 1.00", "FAILURE"))

        try:
            # Get Customer available balance
            cash = cashWithUser(phone)
            # Deduct from vendor and add to customer
            bank_cash = cashWithUser("0240000000")
            updateAccount("0240000000", round(float(bank_cash - amount), 2))
            # Add remaining money to user account
            updateAccount(phone, round(float(cash + amount), 2))

            trans_id = transaction_id()
            confirm_number = addcash_confirmation_number()

            # Insert data into TopUp Collection
            mongo.db.TopUps.insert_one({
                "FirstName": firstname,
                "LastName": lastname,
                "Amount": round(float(amount), 2),
                "SenderNetwork": network,
                "SenderPhone": phone,
                "Email": email,
                "Description": description,
                "TransactionID": trans_id,
                "ConfirmationNumber": confirm_number,
                "CreatedAt": date_time(),
                "Status": "SUCCESS",
                "Service_type": service_type
            })

            jsonResponse = {
                "code": 200,
                "status": "SUCCESS",
                "amount": float(amount),
                "transaction_ID": trans_id,
                "confirmation_Number": confirm_number,
                "message": "Money added successfully to your wallet",
                "response": "Transaction was successful"
            }
            return jsonify(jsonResponse)

        except Exception as e:
            retJson = {
                "code": 409,
                "message": "There was an error while trying to add cash to your account -> , try again!",
                "status": "FAILURE: {0}".format(e.message)
            }
            return jsonify(retJson)

