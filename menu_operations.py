import logging
from exceptions import InsufficientFundsError
from decimal import Decimal,InvalidOperation

def create_account_menu(bank):
    try:
        name=input("Enter name: ")
        balance=Decimal(input("Enter amount: "))
        account=bank.create_account(name,balance)
        account_number=account.account_number
        try:
            bank.save_accounts()
            print("Account created")
            logging.info("Account was created successfully.")
        except OSError as e:
            print(f"Error saving: {e}")
            logging.exception("Failed to save account data.")
            #removes account if saving fails
            bank.accounts.pop(account_number)

     #4 valueerrors defined in create_account of bank.py and an invalid decimal input exception   
    except(ValueError,InvalidOperation) as e:
        print(e)

def deposit_menu(bank):
    #invalid decimal input and account number handling
    try:
        account_number=input("Enter account number to deposit to: ")
        account=bank.find_account(account_number)
        if account is not None:
            og_balance=account.balance
            og_transactions=account.transactions.copy()
            amount=Decimal(input("Enter amount to deposit: "))
            account.deposit(amount)
            #inner try/except for restoring balance and transaction history if deposit save fails
            try:
                bank.save_accounts()
                print("Deposit successful.")
            except OSError as e:
                print(f"Error saving: {e}")
                logging.exception("Failed to save account data.")
                account.balance=og_balance
                account.transactions=og_transactions

    except(ValueError,InvalidOperation) as e:
        print(e)

def withdraw_menu(bank):
    try:
        account_number=input("Enter account number to withdraw from: ")
        account=bank.find_account(account_number)
        if account is not None:
            og_balance=account.balance
            og_transactions=account.transactions.copy()
            amount=Decimal(input("Enter amount to withdraw: "))
            account.withdraw(amount)
            #rollback balance and transactions history if saving withdrawal fails
            try:
                bank.save_accounts()
                print("Withdraw successful.")
            except OSError as e:
                print(f"Error saving: {e}")
                logging.exception("Failed to save account data.")
                account.balance=og_balance
                account.transactions=og_transactions

    except InsufficientFundsError as e:
        print("Insufficient funds.")
        logging.warning("Withdrawal failed due to insufficient funds.")        
    except(ValueError,InvalidOperation) as e:
        print(e)
    
def transfer_menu(bank):
    try:
        sender=input("Enter account number to send money from: ")
        receiver=input("Enter account number to send money to: ")
        account_sender=bank.find_account(sender)
        account_receiver=bank.find_account(receiver)
        if account_sender is not None and account_receiver is not None:
            account_sender_og_balance=account_sender.balance
            account_sender_og_transactions=account_sender.transactions.copy()
            account_receiver_og_balance=account_receiver.balance
            account_receiver_og_transactions=account_receiver.transactions.copy()
            amount=Decimal(input("Enter amount: "))
            bank.transfer(sender,receiver,amount)
            try:
                bank.save_accounts()
                print("Transfer successful")    
            except OSError as e:
                print(f"Error saving: {e}")
                logging.exception("Failed to save account data.")
                #rollback after failed save transfer
                account_sender.balance=account_sender_og_balance
                account_sender.transactions=account_sender_og_transactions
                account_receiver.balance=account_receiver_og_balance
                account_receiver.transactions=account_receiver_og_transactions
    
    except InsufficientFundsError as e:
        print("Insufficient funds.")
        logging.warning("Transfer failed due to insufficient funds.")    
    except(ValueError,InvalidOperation) as e:
        print(e)
    
def balance_menu(bank):
    account_number=input("Enter account number to view balance: ")
    account=bank.find_account(account_number)
    if account is not None:
        print(f"Balance: {account.get_balance()}")

def transaction_menu(bank):
    account_number=input("Enter account number to view transactions: ")
    account=bank.find_account(account_number)
    if account is not None:
        for transaction in account.transaction_generator():
            print(transaction)

def delete_menu(bank):
    account_number=input("Enter number of account to delete: ")
    account=bank.find_account(account_number)
    if account is not None:
        if bank.delete_account(account_number):
            try:
                bank.save_accounts()
                print("Account deleted.")
            except OSError as e:
                print(f"Error saving: {e}")
                logging.exception("Failed to save account data.")
                #account is restored back if saving fails
                bank.accounts[account_number]=account         
                    