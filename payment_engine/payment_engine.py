import sys
from core.engine import PaymentEngine

# TODO what if chargeback does not point back to dispute
# TODO raise any unsupported transaction types


def main():
    path_to_file = sys.argv[1]
    payment_engine = PaymentEngine(print_on_update=True)
    payment_engine.extract_transactions_by_client(path_to_file)
    payment_engine.process_transactions()
    accounts = payment_engine.clients_accounts
    payment_engine.update_clients_accounts_file(accounts)


if __name__ == '__main__':
    main()
