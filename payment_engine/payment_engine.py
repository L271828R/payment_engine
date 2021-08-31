import sys
from core.engine import PaymentEngine 

#TODO make look nice
#TODO test cases
#TODO make test names better
#TODO what if chargeback does not point back to dispute
#TODO raise any unsupported transaction types
#TODO test different file spacing in the csv
#TODO check for file type of the csv file
#TODO output to CLI as instructed


def main():
    path_to_file = sys.argv[1]
    payment_engine = PaymentEngine(write_on_update=False)
    # payment_engine.extract_transactions_by_client(path_to_file)
    data = {'1': [
            {'tx': '1', 'type': 'deposit', 'amount': 1.0},    #  total 1.0 available 1.0 held 0.0
            {'tx': '1', 'type': 'deposit', 'amount': 1.0},    #  duplicate
            ], 
        }
    PaymentEngine.transactions_by_clients = data
    payment_engine.process_transactions()

if __name__ == '__main__':
    main()

