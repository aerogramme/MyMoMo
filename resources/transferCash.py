from flask import jsonify
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.auth import verify_password, users, unauthorized, auth
from common.config import mongo
from common.utils import getNetworkName, cashWithUser, updateAccount, date_time, \
    generateReturnDictionary, UserExist, transactionFee, transaction_id, transfer_confirmation_number

# make sure to retrieve data from database
verify_password(users.get("username"), users.get("password"))
unauthorized



def argParser():
    parser = RequestParser(bundle_errors=True)
    parser.add_argument("firstname", type=str, required=False, help="First Name Required")
    parser.add_argument("lastname", type=str, required=False, help="Last Name Required")
    parser.add_argument("fromPhone", type=str, required=True, help="Sender Phone Number Required:format -> 0243559227")
    parser.add_argument("toPhone", type=str, required=True, help="Receiver Phone Number Required:format -> 0244120126")
    parser.add_argument("amount", type=float, required=True, help="Amount Required")
    parser.add_argument("description", type=float, required=False, help="Description of Transaction")
    parser.add_argument("email", type=str, required=False, help="Enter Email ID")
    return parser

class TransferCash(Resource):
    @auth.login_required
    def post(self):
        # get json data
        args = argParser()
        firstname = args.parse_args().get("firstname")
        lastname = args.parse_args().get("lastname")
        fromPhone = args.parse_args().get("fromPhone")
        toPhone = args.parse_args().get("toPhone")
        amount = args.parse_args().get("amount")
        description = args.parse_args().get("description")
        email = args.parse_args().get("email")
        # extract network name
        fromNetwork = getNetworkName(fromPhone)
        toNetwork = getNetworkName(toPhone)

        if not UserExist(toPhone):
            return jsonify(generateReturnDictionary(301, "Sorry, Mobile Wallet Account does not exists!, create an account.", "FAILURE"))

        cash_from = cashWithUser(fromPhone)
        cash_to = cashWithUser(toPhone)
        bank_cash = cashWithUser("0240000000")
        fees = transactionFee(amount)
        amount_after = round(amount - fees, 2)

        if cash_from <= float(0):
            return jsonify(
                generateReturnDictionary(303, "You are out of money, Please add some cash!", "FAILURE"))
        elif amount <= float(1):
            return jsonify(generateReturnDictionary(304, "The amount entered must be greater than GHS 1.00", "FAILURE"))

        try:
            # add fees to bank
            updateAccount("0240000000", round(float(bank_cash + fees), 2))
            # add to receiving account
            updateAccount(toPhone, round(float(cash_to + amount_after), 2))
            # deduct money from sending account
            updateAccount(fromPhone, round(float(cash_from - amount_after), 2))

            # save to transfer collection
            mongo.db.Transfer.insert_one({
                "FirstName": firstname,
                "LastName": lastname,
                "AmountBeforeFees": round(float(amount), 2),
                "AmountAfterFees": round(float(amount_after), 2),
                "TransactionFees": fees,
                "SenderPhone": fromPhone,
                "ReceiverPhone": toPhone,
                "Email": email,
                "Description": description,
                "ReceiverMobileNetwork": toNetwork,
                "SenderMobileNetwork": fromNetwork,
                "ConfirmationNumber": transfer_confirmation_number(),
                "TransactionID": transaction_id(),
                "Created_At": date_time(),
                "Status":"SUCCESS",
                "response":"Transaction was successful"
            })
            jsonResonpse = {
                "code": 200,
                "status": "SUCCESS",
                "amount": float(amount),
                "transaction_ID": transaction_id(),
                "confirmation_Number": transfer_confirmation_number(),
                "message": "Money transferred successfully from your wallet".format(amount)
            }
            return jsonify(jsonResonpse)
        except Exception as e:
            retJson = {
                "code": 409,
                "message": "There was an error while trying to transfer money from your wallet ->, try again!",
                "status": "FAILURE: {0}".format(e.message)
            }
            return jsonify(retJson)
