from bank import Bank
import logging
from menu_operations import (
    create_account_menu,
    deposit_menu,
    withdraw_menu,
    transfer_menu,
    balance_menu,
    transaction_menu,
    delete_menu
)

if __name__=="__main__":
    
    logging.basicConfig(
        filename="bank.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    bank=Bank()
    bank.load_accounts()
    while True:
        print("1:Create Account")
        print("2:Deposit")
        print("3.Withdraw")
        print("4.Transfer Money")
        print("5.View Balance")
        print("6.Transaction History")
        print("7.View All Accounts")
        print("8.Delete Account")
        print("9.Exit")

        try:
            choice=int(input(""))
        except ValueError:
            print("Invalid input.")
            continue    

        if(choice==1):
            create_account_menu(bank)         

        elif(choice==2):
            deposit_menu(bank)   

        elif(choice==3):
            withdraw_menu(bank)     

        elif choice==4:
            transfer_menu(bank)      

        elif choice==5:
            balance_menu(bank)
        
        elif choice==6:
            transaction_menu(bank)

        elif choice==7:
            bank.list_accounts()

        elif choice==8:
            delete_menu(bank)
            
        elif choice==9:
            print("Exiting")
            break

        else:
            print("Invalid selection.")    