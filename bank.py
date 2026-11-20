import json
import os
import tempfile
from account import Account
from decimal import Decimal
from exceptions import InsufficientFundsError
class Bank:
    def __init__(self):
        self.accounts={}#stores several bank accounts

    def create_account(self,owner,initial_balance):
        initial_balance=Decimal(str(initial_balance))
        if not owner.strip():
            raise ValueError("Name cannot be empty.")
        elif not initial_balance.is_finite():
            raise ValueError("Balance must be finite.")
        elif initial_balance<0:
            raise ValueError("Balance cannot be negative.")
        elif initial_balance!=initial_balance.quantize(Decimal("0.01")):
            raise ValueError("Balance must be entered to 2dp.")
        else:
            account_number=1
            #prevents duplicate account numbers
            while str(account_number) in self.accounts:
                account_number+=1
            account_number=str(account_number)

            account=Account(account_number,owner,initial_balance,[])
            self.accounts[account_number]=account#stored as account_number=key,Account object=value
            return account
            
    def find_account(self,account_number) -> Account|None:
        if account_number not in self.accounts:
            print("Account does not exist")
            return None
        else:
            return self.accounts[account_number]#returns the dictionary value i.e. Account object

    def transfer(self,sender,receiver,amount):
        sender=self.find_account(sender)
        receiver=self.find_account(receiver)
        amount=Decimal(str(amount))
        if sender is None or receiver is None:
            raise ValueError("Error finding.")
        elif sender==receiver:
            raise ValueError("Accounts must not be identical.")
        elif not amount.is_finite():
            raise ValueError("Amount must be finite.")
        elif amount<=0:
            raise ValueError("Amount must be >0.")
        elif amount!=amount.quantize(Decimal("0.01")):
            raise ValueError("Amount must be entered to 2dp.")
        elif sender.balance<amount:
            raise InsufficientFundsError("Insufficient funds.") 
        else:
            sender.balance-=amount
            receiver.balance+=amount
            sender.transactions.append({
                "type":"Transfer",
                "amount":amount,
                "balance_after":sender.balance
            })
            receiver.transactions.append({
                "type":"Transfer",
                "amount":amount,
                "balance_after":receiver.balance
            })
            
    def list_accounts(self):
        if not self.accounts:
            print("No accounts.")
        else:
            for account in self.accounts.values():#returns each account as an Account object
                print(account.to_dict())

    def save_accounts(self):
        #converts value of each account from Account object to dictionary for saving
        data={number:account.to_dict() for number, account in self.accounts.items()}
        #prevents partial writes i.e. corruption to file caused by file writing stopping midway
        temp_path=None#will eventually store name and full path to file e.g. C:\f.tmp
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                delete=False,#prevents automatically deleting the file after closing
                dir=".",#creates the file in the current directory
                suffix=".tmp"
            ) as file:
                temp_path=file.name
                json.dump(data,file,indent=4)

            os.replace(temp_path,"accounts.json")#attempts to replace the file with accounts.json
                                                 #if saving is successful

        finally:#block executes whether file saving is successful or not
            if temp_path is not None and os.path.exists(temp_path):
                os.remove(temp_path)#removes file if save unsuccessful i.e. no os.replace occurs                                      
                                                     
    def load_accounts(self):
        try:
            with open("accounts.json","r") as file:
                data=json.load(file)
                self.accounts={}
                for number,account in data.items():
                    #converting values from str to Decimal for loading json
                    transactions=[
                        {
                          **transaction,
                          "amount":Decimal(str(transaction["amount"])),
                          "balance_after":Decimal(str(transaction["balance_after"]))
                        }
                        for transaction in account["transactions"]
                    ]
                    #converting values to Account objects for loading
                    ac=Account(number,account["owner"],account["balance"],transactions)
                    self.accounts[number]=ac        
        except(FileNotFoundError,json.JSONDecodeError):
            self.accounts={}

    def delete_account(self,account_number)->bool:
        account=self.find_account(account_number)
        if account is not None:
            self.accounts.pop(account_number)
            return True#account was successfully deleted
        else:
            return False#account was not found