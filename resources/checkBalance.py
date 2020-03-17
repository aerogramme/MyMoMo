from flask import jsonify, make_response
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from common.auth import auth, unauthorized, verify_password, users
from common.config import mongo

# make sure to retrieve data from database
from common.utils import generateReturnDictionary, UserExist

verify_password(users.get("username"), users.get("password"))
unauthorized

def argParser():
    parser = RequestParser(bundle_errors=True)
    parser.add_argument("fromPhone", type=str, required=True, help="Phone Number Required:format -> 0243559227")
    return parser


class CheckBalance(Resource):
    @auth.login_required
    def get(self, phone):
        """
       This examples uses FlaskRESTful Resource
       It works also with swag_from, schemas and spec_dict
       ---
       parameters:
         - in: path
           name: username
           type: string
           required: true
         - in: path
           name: password
           type: string
           required: true
         - in: path
           name: phone
           type: string
           required: false
       responses:
         200:
           description: Check Balance on MoMo Wallet
           schema:
             id: CheckBalance
             properties:
               username:
                 type: string
                 description: The username of the user
                 default: freeworldboss
               password:
                 type: string
                 description: The password of the user
                 default: cq#4&Ds6~K+0iwU_
               phone:
                 type: string
                 description: The phone of the user
                 default: 0243559227
        """

        #args = argParser()
        #phone = args.parse_args().get("fromPhone")

        if not UserExist(phone):
            return jsonify(generateReturnDictionary(301, "Sorry, Mobile Wallet Account does not exists!, create an account.", "FAILURE"))

        try:
            retJson = mongo.db.Register.find({
                "Phone": phone
            }, {
                "Password":0,  # projection
                "_id":0,
                "FirstName":0,
                "LastName":0,
                "Email":0,
                "Phone":0,
                "Network":0,
                "Username":0,
                "Password":0,
                "Debt":0,
                "DateTimeCreated":0,
                "apiKeys":0
            })[0]
            return make_response(jsonify(retJson), 200)
        except Exception as e:
            retJson = {
                "code": 409,
                "message": "There was an error while trying to check your wallect balance -> , try again!",
                "status": "FAILURE: {0}".format(e.message)
            }
            return jsonify(retJson)
