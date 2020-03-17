import datetime
import os
import uuid
from binascii import hexlify
from random import random

from passlib.handlers.sha2_crypt import sha256_crypt

from common.config import mongo


def date_time():
    '''current date and time'''
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def getPrettyTime():
    """Get user's pretty current time"""
    rightnow = datetime.datetime.today()
    prettytime = rightnow.ctime()
    return prettytime

def transaction_id():
    '''Generate Transaction ID'''
    return str(uuid.uuid4())

def transfer_confirmation_number(passlen=16):
    ''' Generate API Keys '''
    return "TNF-" + datetime.datetime.now().strftime("%Y%m%d") + "-" + hexlify(os.urandom(passlen)).decode("utf-8")[0:6].upper()

def withdraw_confirmation_number(passlen=16):
    ''' Generate API Keys '''
    return "WDL-" + datetime.datetime.now().strftime("%Y%m%d") + "-" + hexlify(os.urandom(passlen)).decode("utf-8")[0:6].upper()

def addcash_confirmation_number(passlen=16):
    ''' Generate API Keys '''
    return "ADC-" + datetime.datetime.now().strftime("%Y%m%d") + "-" + hexlify(os.urandom(passlen)).decode("utf-8")[0:6].upper()

def getNetworkName(phoneNumber):
    '''get network name given phone number'''
    switcher = {"024": "MTN",
                "054": "MTN",
                "055": "MTN",
                "059": "MTN",
                "026": "AIRTEL",
                "056": "AIRTEL",
                "027": "TIGO",
                "057": "TIGO",
                "020": "VODAFONE",
                "030": "VODAFONE",
                "050": "VODAFONE"
                }
    return switcher.get(phoneNumber[0:3], "Unsupported phone number for network detected")

def generateApiKeys(passlen=16):
    ''' Generate API Keys '''
    return hexlify(os.urandom(passlen)).decode("utf-8")

def gen_reset_password(passlen=16):
    '''generate reset password'''
    s = "!_*&abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ#@(~+"
    generated_password = "".join(random.sample(s, passlen))
    return str(generated_password)

###########################################################
# 	FUNC SECTION
###########################################################
def verifyPw(phone, password):
    if not UserExist(phone):
        return False

    hashed_pw = mongo.db.Register.find_one({"Phone": phone})["Password"]

    if sha256_crypt.verify(password, hashed_pw):
        return True
    else:
        return False

def verifyCredentials(phone, password):
    if not UserExist(phone):
        return generateReturnDictionary(301, "Invalid Username/Phone", "FAILURE"), True

    correct_pw = verifyPw(phone, password)

    if not correct_pw:
        return generateReturnDictionary(302, "Incorrect Password", "FAILURE"), True

    return None, False

def UserExist(phone):
    '''Check if Phone Number Exist in DB'''
    userAccount = mongo.db.Register
    if userAccount.count_documents({"Phone": phone}) == 0:
        return False
    else:
        return True

def cashWithUser(phone):
    cash = mongo.db.Register.find_one({
        "Phone": phone
    })["Balance"]
    return cash


def debtWithUser(phone):
    debt = mongo.db.Register.find_one({
        "Phone": phone
    })["Debt"]
    return debt


def generateReturnDictionary(code, msg, status):
    retJson = {
        "code": code,
        "message": msg,
        "status": status
    }
    return retJson

def updateAccount(phone, balance):
    try:
        mongo.db.Register.update_one({
            "Phone": phone
        }, {
            "$set": {
                "Balance": round(float(balance), 2)
            }
        })
    except Exception as e:
        print("Account Update Not Successful {0}".format(e.message))

def updateDebt(phone, balance):
    mongo.db.Register.update_one({
        "Phone": phone
    }, {
        "$set": {
            "Debt": round(float(balance), 2)
        }
    })

def transactionFee(amount):
    ''' 1% Transaction Fees '''
    return round(amount * 0.01, 2)

