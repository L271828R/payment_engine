import pytest
# from payment_engine import PaymentEngine
# from payment_engine import PaymentEngine
from payment_engine.core.engine import PaymentEngine
#TODO change ids to numbers as per doc. two of them

def test_base_happy_path():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 1.0}, 
            {'tx': '3', 'type': 'deposit', 'amount': 2.0}, 
            {'tx': '4', 'type': 'withdrawal', 'amount': 1.5}], 
        '2': [
            {'tx': '2', 'type': 'deposit', 'amount': 2.0}, 
            {'tx': '5', 'type': 'withdrawal', 'amount': 3.0}]
        }
    expected = {'1': 
        {'client':'1', 'total': 1.5, 'available': 1.5, 'held': 0.0, 'locked': 'false'},
         '2': {'client': '2', 'total': 2.0, 'available': 2.0, 'held': 0.0, 'locked':'false'}}
    transaction_engine = PaymentEngine(write_on_update=False)
    transaction_engine.transactions_by_clients = data
    transaction_engine.process_transactions()
    results = transaction_engine.clients_accounts
    assert (expected == results)

def test_one_dispute_one_client():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 1.0}, 
            {'tx': '3', 'type': 'deposit', 'amount': 2.0}, 
            {'tx': '4', 'type': 'withdrawal', 'amount': 1.5},
            {'tx': '1', 'type': 'dispute', }
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.5, 'available': 0.5, 'held': 1.0, 'locked':'false'}}
    transaction_engine = PaymentEngine(write_on_update=False)
    transaction_engine.transactions_by_clients = data
    transaction_engine.process_transactions()
    results = transaction_engine.clients_accounts
    assert (expected == results)

def test_one_dispute_one_client_large():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 2.0}, 
            {'tx': '3', 'type': 'deposit', 'amount': 1.0}, 
            {'tx': '4', 'type': 'withdrawal', 'amount': 1.5},
            {'tx': '1', 'type': 'dispute', },
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.5, 'available': -0.5, 'held': 2.0, 'locked':'false'}}
    transaction_engine = PaymentEngine(write_on_update=False)
    transaction_engine.transactions_by_clients = data
    transaction_engine.process_transactions()
    results = transaction_engine.clients_accounts
    assert (expected == results)

def test_one_dispute_one_resolve_one_client():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 1.0},    #  total 1.0 available 1.0 held 0.0
            {'tx': '3', 'type': 'deposit', 'amount': 2.0},    #  total 3.0 available 3.0 held 0.0
            {'tx': '4', 'type': 'withdrawal', 'amount': 1.5}, #  total 1.5  available 1.5 held 0.0
            {'tx': '1', 'type': 'dispute', },                 #  total 1.5  available 0.5 held 1.0
            {'tx': '5', 'type': 'withdrawal', 'amount': 1.5}, #x total 1.5 available 0.5 held 1.0
            {'tx': '1', 'type': 'resolve', },                 #  total 1.5 available 1.5 held 0.0
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.5, 'available': 1.5, 'held': 0.0, 'locked':'false'}}
    transaction_engine = PaymentEngine(write_on_update=False)
    transaction_engine.transactions_by_clients = data
    transaction_engine.process_transactions()
    results = transaction_engine.clients_accounts
    assert (expected == results)


def test_one_dispute_one_chargeback():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 1.0},    #  total 1.0 available 1.0 held 0.0
            {'tx': '3', 'type': 'deposit', 'amount': 2.0},    #  total 3.0 available 3.0 held 0.0
            {'tx': '4', 'type': 'withdrawal', 'amount': 1.5}, #  total 1.5  available 1.5 held 0.0
            {'tx': '1', 'type': 'dispute', },                 #  total 1.5  available 0.5 held 1.0
            {'tx': '5', 'type': 'withdrawal', 'amount': 1.5}, #x total 1.5 available 0.5 held 1.0
            {'tx': '1', 'type': 'chargeback', },              #  total 0.5 available 0.5 held 0.0 locked
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 0.5, 'available': 0.5, 'held': 0.0, 'locked':'true'}}
    transaction_engine = PaymentEngine(write_on_update=False)
    transaction_engine.transactions_by_clients = data
    transaction_engine.process_transactions()
    results = transaction_engine.clients_accounts
    assert (expected == results)



def test_precision():
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 1.0010},    #  total 1.0 available 1.0 held 0.0
            {'tx': '4', 'type': 'withdrawal', 'amount': 0.0001}, #  total 1.5  available 1.5 held 0.0
            ], 
        }
    expected = {'1': 
        {'client': '1', 'total': 1.0009, 'available': 1.0009, 'held': 0.0, 'locked':'false'}}
    transaction_engine = PaymentEngine(write_on_update=False)
    transaction_engine.transactions_by_clients = data
    transaction_engine.process_transactions()
    results = transaction_engine.clients_accounts
    assert (expected == results)
