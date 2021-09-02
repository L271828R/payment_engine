from core.engine import PaymentEngine
from core import python_version_validation

# TODO what if chargeback does not point back to dispute
# TODO raise any unsupported transaction types


def main():
    # path_to_file = sys.argv[1]
    path_to_file = "tests/test_files/transactions_dup_dispute.csv"
    payment_engine = PaymentEngine(print_on_update=True)
    payment_engine.extract_transactions_by_client(path_to_file)
    payment_engine.process_transactions()
    accounts = payment_engine.clients_accounts
    payment_engine.update_clients_accounts_file(accounts)


if __name__ == '__main__':
    if python_version_validation.validate(3,4):
        main()
