from payment_engine.core.engine import PaymentEngine
from payment_engine.core.python_version_validation import validate



def test_precision():
    data = {'1':
        [
            {'tx': '1', 'type': 'deposit', 'amount': 1.00111}, 
            {'tx': '3', 'type': 'deposit', 'amount': 2.03333}, 
            {'tx': '4', 'type': 'withdrawal', 'amount': 1.5}
        ],
        '2':
        [
            {'tx': '5', 'type': 'deposit', 'amount': 1.00111}, 
            {'tx': '6', 'type': 'deposit', 'amount': 2.03333}, 
            {'tx': '7', 'type': 'withdrawal', 'amount': 1.5}
        ],
        }
    expected = {'1': 
        {'client':'1', 'total': 1.5344, 'available': 1.5344, 'held': 0.0, 'locked': 'false'},
        '2':
        {'client':'2', 'total': 1.5344, 'available': 1.5344, 'held': 0.0, 'locked': 'false'}
        }
    payment_engine = PaymentEngine()
    payment_engine.transactions_by_clients = data
    payment_engine.process_transactions()
    results = payment_engine.client_accounts
    assert (expected == results)
