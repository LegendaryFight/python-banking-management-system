from utils import validate_amount, log_operation
from decimal import Decimal
from exceptions import InsufficientFundsError
class Account:
    def __init__(self,account_number,owner,balance,transactions):
        if not account_number.strip():
            raise ValueError("Account number can't be empty")
        elif not account_number.isnumeric():
            raise ValueError("Account number is invalid")
        else:
            self.account_number=account_number            

        if not owner.strip():
            raise ValueError("Name can't be empty")
        else:
            self.owner=owner

        balance=Decimal(str(balance))
        if not balance.is_finite():
            raise ValueError("Amount must be finite.")
        elif balance<0:
            raise ValueError("Balance can't be negative")
        elif balance!=balance.quantize(Decimal("0.01")):
            raise ValueError("Amount must be entered to 2dp.")
        else:
            self.balance=balance

        self.transactions=transactions if transactions is not None else []

    @validate_amount
    def deposit(self,amount):
        self.balance+=amount
        self.transactions.append({
            "type":"Deposit",
            "amount":amount,
            "balance_after":self.balance
        })

    @validate_amount
    def withdraw(self,amount):
        if amount>self.balance:
            raise InsufficientFundsError("Insufficient funds.") 
        else:
            self.balance-=amount
            self.transactions.append({
                "type":"Withdraw",
                "amount":amount,
                "balance_after":self.balance
            })
    @log_operation
    def get_balance(self):
        return self.balance

    @log_operation
    def get_transactions(self):
        return self.transactions

    def to_dict(self):
        return{
        #Decimal is not a data type accepted by json so convert all decimal values to str for saving
            "account_number":self.account_number,
            "owner":self.owner,
            "balance":str(self.balance),
            "transactions":[
                {
                  **transaction,#copy of original dictionary created to change Decimal to str
                  "amount":str(transaction["amount"]),
                  "balance_after":str(transaction["balance_after"])
                }
                for transaction in self.transactions
            ]
        }

    def transaction_generator(self):
        for transaction in self.transactions:
            yield transaction