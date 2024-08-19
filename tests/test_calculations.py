from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import pytest


@pytest.fixture
def zero_bank_account():
    return BankAccount()
@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [
    (1, 2, 3),
    (3, 4, 7),
    (5, 6, 11),
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(9, 4) == 36




def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50

def test_bank_defualt_amount(zero_bank_account):
    assert zero_bank_account.balance == 0
    
def test_withdraw(bank_account):
    bank_account.withdraw(20)
    assert bank_account.balance == 30


def test_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 100

def test_collect_intrest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (50, 20, 30),
    (1000, 800, 200),
])


def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
