import sys
from core.engine import PaymentEngine 

#TODO make look nice
#TODO test cases


def main():
    path_to_file = sys.argv[1]
    payment_engine = PaymentEngine(write_on_update=False)
    payment_engine.extract_transactions_by_client(path_to_file)
    payment_engine.process_transactions()

if __name__ == '__main__':
    main()

