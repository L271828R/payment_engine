from payment_engine.core.engine import PaymentEngine
import pytest

def test_neg_one_dispute_one_chargeback_lock_logic():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 1.0},    #  total 1.0 available 1.0 held 0.0
            {'tx': '3', 'type': 'deposit', 'amount': 2.0},    #  total 3.0 available 3.0 held 0.0
            {'tx': '4', 'type': 'withdrawal', 'amount': 1.5}, #  total 1.5  available 1.5 held 0.0
            {'tx': '1', 'type': 'dispute', },                 #  total 1.5  available 0.5 held 1.0
            {'tx': '5', 'type': 'withdrawal', 'amount': 1.5}, #x total 1.5 available 0.5 held 1.0
            {'tx': '1', 'type': 'chargeback', },              #  total 0.5 available 0.5 held 0.0 locked
            {'tx': '5', 'type': 'withdrawal', 'amount': 1.5}  #  total 0.5 available 0.5 held 0.0 locked
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 0.5, 'available': 0.5, 'held': 0.0, 'locked':'true'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)


def test_neg_duplicate_deposits():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 1.0},    #  total 1.0 available 1.0 held 0.0
            {'tx': '1', 'type': 'deposit', 'amount': 1.0},    #  duplicate
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.0, 'available': 1.0, 'held': 0.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)

def test_neg_duplicate_withdrawals():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 2.0},    #  total 2.0 available 2.0 held 0.0
            {'tx': '2', 'type': 'withdrawal', 'amount': 1.0}, #  total 1.0 available 1.0 held 0.e
            {'tx': '2', 'type': 'withdrawal', 'amount': 1.0}  #  duplicate
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.0, 'available': 1.0, 'held': 0.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)

def test_neg_duplicate_dispute():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 2.0},    #  total 2.0 available 2.0 held 0.0
            {'tx': '2', 'type': 'withdrawal', 'amount': 1.0}, #  total 1.0 available 1.0 held 0.0
            {'tx': '1', 'type': 'dispute', },                 #  total 1.0 available -1.0 held 2.0
            {'tx': '1', 'type': 'dispute', }                  #  duplicate
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.0, 'available': -1.0, 'held': 2.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)


def test_neg_duplicate_chargeback():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 2.0},    #  total 2.0 available 2.0 held 0.0
            {'tx': '2', 'type': 'withdrawal', 'amount': 1.0}, #  total 1.0 available 1.0 held 0.0
            {'tx': '1', 'type': 'dispute', },                 #  total 1.0 available -1.0 held 2.0
            {'tx': '1', 'type': 'chargeback', },              #  total -1.0 available -1.0 held 0.0 
            {'tx': '1', 'type': 'chargeback', }               #  duplicate
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': -1.0, 'available': -1.0, 'held': 0.0, 'locked':'true'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)

def neg_duplicate_resolves():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 2.0},    #  total 2.0 available 2.0 held 0.0
            {'tx': '2', 'type': 'withdrawal', 'amount': 1.0}, #  total 1.0 available 1.0 held 0.0
            {'tx': '3', 'type': 'dispute', },                 #  total -1.0 available 1.0 held -2.0
            {'tx': '3', 'type': 'resolve', },                  #  total 1.0 available 1.0 held 0.0
            {'tx': '3', 'type': 'resolve', }                  #  duplicate
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.0, 'available': 1.0, 'held': 0.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)



def test_neg_duplicate_chargebacks_with_negative_held():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 2.0},    #  total 2.0 available 2.0 held 0.0
            {'tx': '2', 'type': 'withdrawal', 'amount': 1.0}, #  total 1.0 available 1.0 held 0.0
            {'tx': '3', 'type': 'dispute', },                 #  total -1.0 available 1.0 held -2.0
            {'tx': '3', 'type': 'chargeback', }               #  total 1.0 available 1.0 held 0.0
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.0, 'available': 1.0, 'held': 0.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)

def test_neg_dispute_on_a_withdrawal():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 2.0},    #  total 2.0 available 2.0 held 0.0
            {'tx': '2', 'type': 'withdrawal', 'amount': 1.0}, #  total 1.0 available 1.0 held 0.0
            {'tx': '2', 'type': 'dispute', }                  #  total 1.0 available 1.0 held 0.0
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.0, 'available': 1.0, 'held': 0.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)


def test_neg_dispute_on_a_withdrawal_and_chargeback():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 2.0},    #  total 2.0 available 2.0 held 0.0
            {'tx': '2', 'type': 'withdrawal', 'amount': 1.0}, #  total 1.0 available 1.0 held 0.0
            {'tx': '2', 'type': 'dispute', },                  #  total 1.0 available 1.0 held 0.0
            {'tx': '2', 'type': 'chargeback', }               #  total 1.0 available 1.0 held 0.0
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.0, 'available': 1.0, 'held': 0.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)

def test_neg_unsupported_transaction():
    data = {'1': [
            {'tx': '1', 'type': 'unsupported', 'amount': 2.0}    #  total 2.0 available 2.0 held 0.0
            ], 
        }
    with pytest.raises(Exception) as e:
        payment_engine = PaymentEngine()
        payment_engine.transactions_by_clients = data
        payment_engine.process_transactions()
    assert(str(e.value) == "unsupported is not supported")

def test_neg_withdrawal_greater_than_deposit():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 2.0},    #  total 2.0 available 2.0 held 0.0
            {'tx': '2', 'type': 'withdrawal', 'amount': 3.0}, #  total 1.0 available 1.0 held 0.0
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 2.0, 'available': 2.0, 'held': 0.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)