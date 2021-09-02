import pytest
from payment_engine.core.engine import PaymentEngine

def test_read_csv_file_version1():
    path_to_file = "tests/test_files/transactions.csv"
    payment_engine = PaymentEngine()
    payment_engine.extract_transactions_by_client(path_to_file)
    results = payment_engine.transactions_by_clients
    expected = {
            "1": [
                {"type":"deposit", "tx": "1", "amount":1.0},
                {"type":"deposit", "tx": "3", "amount":2.0},
                {"type":"withdrawal", "tx": "4", "amount":1.5}],
            "2": [
                {"type":"deposit", "tx": "2", "amount":2.0},
                {"type":"withdrawal", "tx": "5", "amount":3.0}]}
    assert (expected == results)

def test_read_csv_file_version2():
    path_to_file = "tests/test_files/transactions2.csv"
    payment_engine = PaymentEngine()
    payment_engine.extract_transactions_by_client(path_to_file)
    results = payment_engine.transactions_by_clients
    expected = {
            "1": [
                {"type":"deposit", "tx": "1", "amount":1.0},
                {"type":"deposit", "tx": "3", "amount":2.0},
                {"type":"withdrawal", "tx": "4", "amount":1.5}],
            "2": [
                {"type":"deposit", "tx": "2", "amount":2.0},
                {"type":"withdrawal", "tx": "5", "amount":3.0}]}
    assert (expected == results)


def test_happy_path_file_version():
    path_to_file = "tests/test_files/transactions.csv"
    expected = {'1': 
        {'client':'1', 'total': 1.5, 'available': 1.5, 'held': 0.0, 'locked': 'false'},
         '2': {'client': '2', 'total': 2.0, 'available': 2.0, 'held': 0.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.extract_transactions_by_client(path_to_file)
    payment_engine.process_transactions()
    results = payment_engine.clients_accounts
    assert (expected == results)


def test_happy_path_file_version2():
    path_to_file = "tests/test_files/transactions2.csv"
    expected = {'1': 
        {'client':'1', 'total': 1.5, 'available': 1.5, 'held': 0.0, 'locked': 'false'},
         '2': {'client': '2', 'total': 2.0, 'available': 2.0, 'held': 0.0, 'locked':'false'}}
    payment_engine = PaymentEngine()
    payment_engine.extract_transactions_by_client(path_to_file)
    payment_engine.process_transactions()
    results = payment_engine.clients_accounts
    assert (expected == results)

def test_unsupported_file_type():
    path_to_file = "tests/test_files/transactions.abc"
    payment_engine = PaymentEngine()
    with pytest.raises(Exception) as e:
        payment_engine.extract_transactions_by_client(path_to_file)
    assert(str(e.value) == "FILE NOT SUPPORTED, CSV ONLY")