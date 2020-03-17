
#!/usr/bin/python
########################################################
__author__ = 'Theophilus Siameh'
__author_email__ = 'theodondre@gmail.com'
__copyright__ = 'Copyright (C) 2020 Theophilus Siameh'
__version__ = 1.0
########################################################

from flasgger import Swagger
from flask import Flask
# from flask_mail import Mail
from flask_pymongo import PyMongo
from flask_restful import Api
from flask import jsonify

from common.cred import data

##################################################
# API SECTION
##################################################
from resources.checkBalance import CheckBalance
from resources.addCash import AddCash
from resources.getTransactionStatus import GetTransactionStatus
from resources.transferCash import TransferCash
from resources.withdrawCash import WithdrawCash
from resources.accountVerification import AccountVerification

# MongoDB Credentials
DB = data.get("DB")
USERNAME = data.get("username")
PASSWORD = data.get("password")

app = Flask(__name__)
swagger = Swagger(app)

app.config['SECRET_KEY'] = "MobileMoney"
app.config["MONGO_URI"] = "mongodb+srv://{0}:{1}@mobilemoney-q3w48.mongodb.net/{2}?retryWrites=true&w=majority".format(USERNAME, PASSWORD, DB)

mongo = PyMongo(app)
api = Api(app)


@app.route("/")
def get_initial_response():
    """Welcome message for the API."""
    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to the MyMoMo.io API'
    }
    return jsonify(message)



# End Points
api.add_resource(AddCash, '/momo/api/v1/addcash', endpoint = '/addcash')
api.add_resource(TransferCash, '/momo/api/v1/transfer', endpoint = '/transfer')
#api.add_resource(CheckBalance, '/momo/api/v1/balance', endpoint = '/balance')
api.add_resource(CheckBalance, '/momo/api/v1/balance/<string:phone>')
api.add_resource(WithdrawCash, '/momo/api/v1/withdraw', endpoint = '/withdraw')
api.add_resource(AccountVerification, '/momo/api/v1/account-verification/<string:phone>')
api.add_resource(GetTransactionStatus, '/momo/api/v1/get-transaction-status/<string:transaction_id>', endpoint = '/get-transaction-status')

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=80,debug=True)
    app.run(debug=True)

