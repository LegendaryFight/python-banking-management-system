from bank import Bank
from decimal import Decimal
import unittest
from exceptions import InsufficientFundsError
class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank=Bank()
        self.account=self.bank.create_account("a",Decimal("100.00"))
        self.account2=self.bank.create_account("b",Decimal("100.00"))

    def test_create_account(self):
        self.assertEqual(self.account.account_number,"1")
        self.assertEqual(self.account.owner,"a")
        self.assertEqual(self.account.balance, Decimal("100.00"))

    def test_transfer(self):
        self.bank.transfer("1","2",Decimal("50.00"))
        self.assertEqual(self.account.balance,Decimal("50.00"))
        self.assertEqual(self.account2.balance,Decimal("150.00"))

    def test_transfer_insufficient_funds(self):
        with self.assertRaisesRegex(InsufficientFundsError,"Insufficient funds"):
            self.bank.transfer("1","2",Decimal("100.01"))
        self.assertEqual(self.account.balance,Decimal("100.00"))
        self.assertEqual(self.account2.balance,Decimal("100.00")) 

    def test_transfer_same_account(self):
        with self.assertRaises(ValueError):
            self.bank.transfer("1","1",Decimal("50"))
        self.assertEqual(self.account.balance,Decimal("100.00"))

    def test_delete_account(self):
        result=self.bank.delete_account("1")
        self.assertTrue(result)
        self.assertIn("2",self.bank.accounts)
        self.assertNotIn("1",self.bank.accounts)

    def test_delete_nonexistent_account(self):
        result=self.bank.delete_account("45")
        self.assertFalse(result)
        self.assertIn("1",self.bank.accounts)
        self.assertIn("2",self.bank.accounts)