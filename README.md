# Python Banking Management System

A command-line banking management application developed in Python using object-oriented programming (OOP). The system supports account management, financial transactions, persistent storage, and automated testing.

## Features

- Create and delete bank accounts
- Deposit and withdraw money
- Transfer money between accounts
- View account balances and transaction histories
- List all registered accounts
- Save and load account information using JSON
- Validate monetary amounts using Python's `Decimal`
- Handle invalid operations and insufficient funds
- Use atomic file replacement to reduce the risk of corrupted data
- Restore account data when saving operations fail
- Log errors and important operations

## Technologies

- Python 3.11
- Object-Oriented Programming (OOP)
- JSON
- Decimal
- Logging
- unittest
- unittest.mock
- tempfile and os

## Project Structure

```text
python-banking-management-system/
├── account.py
├── bank.py
├── main.py
├── menu_operations.py
├── utils.py
├── exceptions.py
├── test_account.py
├── test_bank.py
├── test_persistence.py
├── README.md
└── .gitignore
```

## How to Run

1. Install Python 3.11 or newer.
2. Clone the repository.
3. Open a terminal in the project directory.
4. Run:

```bash
python main.py
```

The application displays an interactive menu for managing accounts and transactions.

## Running Tests

Run all automated tests using:

```bash
python -m unittest discover -v
```

The test suite covers account operations, transfers, validation, persistence, and simulated file-saving failures.

## Data Persistence

Account information and transaction histories are stored locally in `accounts.json`, which is created when account data is saved.

The application uses temporary files and atomic replacement to reduce the risk of incomplete writes. Rollback mechanisms restore in-memory account data when saving fails.

## Purpose

This project was independently developed to strengthen practical Python software engineering skills, including OOP, modular design, data validation, exception handling, persistence, debugging, and automated testing.
