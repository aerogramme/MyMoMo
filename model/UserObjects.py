class UsersRegistration(object):
    def __init__(self, firstname, lastname, email, phone, network, username, password, balance, debt):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.phone = phone
        self.network = network
        self.username = username
        self.password = password
        self.balance = balance
        self.debt = debt

class AddCash(object):
    def __init__(self, username, amount, network, phone):
        self.username = username
        self.amount  = amount
        self.network = network
        self.phone = phone


class WithdrawCash(object):
    def __init__(self,username, amountBeforeFees, amountAfterFees, fromPhone, toPhone, toNetwork,fromNetwork):
        self.username = username
        self.amountBeforeFees = amountBeforeFees
        self.amountAfterFees = amountAfterFees
        self.fromPhone = fromPhone
        self.toPhone = toPhone
        self.toNetwork = toNetwork
        self.fromNetwork = fromNetwork

class TransferCash(object):
    def __init__(self,username, amountBeforeFees, amountAfterFees, fromPhone, toPhone, toNetwork,fromNetwork):
        self.username = username
        self.amountBeforeFees = amountBeforeFees
        self.amountAfterFees = amountAfterFees
        self.fromPhone = fromPhone
        self.toPhone = toPhone
        self.toNetwork = toNetwork
        self.fromNetwork = fromNetwork

class CheckBalance(object):
    def __init__(self):
        pass
