import sys
from core.engine import PaymentEngine
from core import python_version_validation

# TODO what if chargeback does not point back to dispute

def main():
    path_to_file = sys.argv[1]
    payment_engine = PaymentEngine(print_on_update=False)
    payment_engine.extract_transactions_by_client(path_to_file)
    payment_engine.process_transactions()
    client_accounts = payment_engine.client_accounts
    payment_engine.print_to_stdout(client_accounts)


if __name__ == '__main__':
    if python_version_validation.validate(3,4):
        main()
