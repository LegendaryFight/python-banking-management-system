from bank import Bank
from decimal import Decimal
from unittest.mock import patch#provides mocking tools to temporarily replace a function, method
import os                      #or object with a substitute to safely test
import tempfile
import unittest
from menu_operations import(
    deposit_menu,withdraw_menu,transfer_menu,delete_menu,create_account_menu
)

class TestPersistence(unittest.TestCase):
    def setUp(self):
        #creating temporary folder to unit test saving/loading json without changing accounts.json
        self.og_directory=os.getcwd()#saves og folder to return to it after finishing
        self.temp_directory=tempfile.TemporaryDirectory()#creates the temporary directory
        os.chdir(self.temp_directory.name)#changes to the temporary directory
        self.bank=Bank()
        self.account=self.bank.create_account("a",Decimal("100.00"))

    def test_save_accounts(self):
        self.bank.save_accounts()
        result=os.path.exists("accounts.json")
        self.assertTrue(result)

    def test_load_accounts(self):
        self.bank.save_accounts()
        bank2=Bank()
        bank2.load_accounts()
        result=bank2.accounts["1"]
        self.assertIn("1",self.bank.accounts)
        self.assertEqual(result.balance,Decimal("100.00"))
        self.assertEqual(result.owner,"a")

    def test_save_failure(self):
        #replaces os.replace() with a mock and side_effect tells mock to raise exception whenever
        #it's called.
        with patch("bank.os.replace",side_effect=OSError("Disk error")):
            with self.assertRaises(OSError):  
                self.bank.save_accounts()
            result=os.path.exists("accounts.json")
            self.assertFalse(result)

    def test_deposit_save_failure(self):
        with patch("builtins.input",side_effect=["1","10.00"]):#mock account number and deposit input
                                                               #because deposit_menu needs these inputs 
            #replaces save_accounts() of self.bank.save_accounts() with mock
            with patch.object(self.bank,"save_accounts",side_effect=OSError("Disk error")):
                deposit_menu(self.bank)#rollback code in deposit_menu implemented

        self.assertEqual(self.account.balance,Decimal("100.00"))
        self.assertEqual(self.account.transactions,[])

    def test_withdrawal_save_failure(self):
        with patch("builtins.input",side_effect=["1","10.00"]):#account number and withdrawal
            with patch.object(self.bank,"save_accounts",side_effect=OSError("Disk error")):
                withdraw_menu(self.bank)
        self.assertEqual(self.account.balance,Decimal("100.00"))
        self.assertEqual(self.account.transactions,[])

    def test_transfer_save_failure(self):
        self.account2=self.bank.create_account("b",Decimal("100.00"))
        with patch("builtins.input",side_effect=["1","2","10.00"]):
            with patch.object(self.bank,"save_accounts",side_effect=OSError("Disk error")):
                transfer_menu(self.bank)
        self.assertEqual(self.account.balance,Decimal("100.00"))
        self.assertEqual(self.account.transactions,[])
        self.assertEqual(self.account2.balance,Decimal("100.00"))
        self.assertEqual(self.account2.transactions,[])

    def test_delete_save_failure(self):
         with patch("builtins.input",side_effect=["1"]):
            with patch.object(self.bank,"save_accounts",side_effect=OSError("Disk error")):
                delete_menu(self.bank)
            self.assertIn("1",self.bank.accounts)

    def test_create_save_failure(self):
        with patch("builtins.input",side_effect=["a","100.00"]):
            with patch.object(self.bank,"save_accounts",side_effect=OSError("Disk error")):
                create_account_menu(self.bank)
        self.assertNotIn("2",self.bank.accounts)#verifies new account removed after save fail
        self.assertIn("1",self.bank.accounts)#other remains

    def test_save_call(self):
        with patch("bank.os.replace") as mock_replace:
            self.bank.save_accounts()
            args,kwargs=mock_replace.call_args#retrieves the arguments of os.replace()
        mock_replace.assert_called_once()#verifies that os.replace() was called exactly once.
        self.assertEqual(len(args),2)
        self.assertTrue(args[0].endswith(".tmp"))  
        self.assertEqual(args[1],"accounts.json")
        self.assertEqual(len(kwargs),0)
        result=os.path.exists("accounts.json")
        self.assertFalse(result)       

    def tearDown(self):
        os.chdir(self.og_directory)
        self.temp_directory.cleanup()