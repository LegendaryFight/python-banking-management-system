from account import Account
from decimal import Decimal
import unittest
from exceptions import InsufficientFundsError

class TestAccount(unittest.TestCase):
    def setUp(self):
        self.account=Account("1","a",Decimal("50.00"),[])
        
    def test_deposit(self):
        ac1=Account("1","John",Decimal("100.00"),[])
        ac1.deposit(Decimal("50.00"))
        self.assertEqual(ac1.balance,Decimal("150.00"))

    def test_withdraw(self):
        self.account.withdraw(Decimal("10.00"))
        self.assertEqual(self.account.balance,Decimal("40.00"))

    def test_insufficient_funds(self):
        with self.assertRaises(InsufficientFundsError) as context:
            self.account.withdraw(Decimal("100.00"))
        self.assertEqual(str(context.exception),"Insufficient funds.")
        self.assertEqual(self.account.balance,Decimal("50.00"))

    def test_negative_deposit(self):
        with self.assertRaises(ValueError):
            self.account.deposit(Decimal("-50.00"))
        self.assertEqual(self.account.balance,Decimal("50.00"))    
        
    def test_invalid_precision(self):
        with self.assertRaises(ValueError):
            self.account.deposit(Decimal("50.122"))
        self.assertEqual(self.account.balance,Decimal("50.00"))      