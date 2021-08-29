import sys
import csv
from collections import OrderedDict

#TODO need to sort by tx id ( test )
#TODO assert ids of are valid int type, there are two
#TODO change ids to numbers as per doc. two of them
#TODO test for precision otherwise bad score
#TODO disputes and resolves may happen at any time will need to 
#recalculate

class TransactionEngine():
    def __init__(self, write_on_update=True):
        self.write_on_update = write_on_update
        self.transactions_by_client = None
        self.totals_by_client = None

    def extract_transactions_by_client(self, path_to_file):
        self.transactions_by_clients = self.transaction_file_reader(path_to_file)

    def process_transactions(self):
        self.clients_accounts = self._process_transactions(self.transactions_by_clients)

    def update_clients_accounts_file(self, clients_accounts):
        with open("clients_accounts.csv", "w") as csvfile:
            fieldnames = ['client', 'available', 'held', 'total', 'locked']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for client in clients_accounts:
                row = clients_accounts[client]
                writer.writerow(row)


    def transaction_file_reader(self, path_to_file):
        transactions_by_clients = {}
        with open(path_to_file) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                trans_type = row['type'].replace(" ","")
                client_id  = row['client'].replace(" ","")
                tx         = row['tx'].replace(" ","")
                try:
                    amount     = float(row['amount'])
                except ValueError:
                    amount     = 0
                parsed_row = {'type': trans_type, 
                        'client_id': client_id,
                        'tx': tx,
                        'amount': amount}
                if client_id not in transactions_by_clients:
                    transactions_by_clients[client_id] = []
                transactions_by_clients[client_id].append({'tx': tx,'type':trans_type, 'amount': amount})
            return transactions_by_clients

    def execute_dispute(self, tx_id, transactions):
        print('INSIDE EXECUTED DISPUTES')
        input()
        pass

    def _process_transactions(self, transactions_by_clients):
        clients = {}
        disputed_resolution = {}
        for client in transactions_by_clients:
            need_to_recalculate = True
            tx_id_amount_lookup = {}
            total = 0.0
            held = 0.0
            available = 0.0
            locked = 'false'
            for transaction in transactions_by_clients[client]:
                trans_type = transaction['type']
                tx_id = transaction['tx']
                if trans_type == "deposit":
                    if tx_id not in disputed_resolution:
                        tx_id_amount_lookup[tx_id] = transaction["amount"]
                        total += float(transaction["amount"])
                        available += float(transaction["amount"])
                        clients[client] = {"client": client, "total" : total, \
                            "available": available, "held": held, "locked": locked}
                        assert(total == available + held)
                        if self.write_on_update:
                            self.update_clients_accounts_file(clients)

                elif trans_type == "withdrawal":
                    tx_id_amount_lookup[tx_id] = transaction["amount"]
                    amount = float(transaction["amount"])
                    if amount <= available: 
                        total -= float(transaction["amount"])
                        available -= float(transaction["amount"])
                        clients[client] = {"client": client, "total" : total, \
                            "available": available, "held": held, "locked": locked}
                        assert(total == available + held)
                        if self.write_on_update:
                            self.update_clients_accounts_file(clients)
                elif trans_type == "dispute":
                    if tx_id in tx_id_amount_lookup and tx_id not in disputed_resolution:
                        amount = tx_id_amount_lookup[tx_id]
                        available -= amount
                        held += amount
                        disputed_resolution[tx_id] = None
                        total = available + held
                        clients[client] = {"client": client, "total" : total, \
                            "available": available, "held": held, "locked": locked}
                        assert(total == available + held)
                        if self.write_on_update:
                            self.update_clients_accounts_file(clients)
                elif trans_type == "resolve":
                    if tx_id in tx_id_amount_lookup and \
                        tx_id in disputed_resolution and \
                        disputed_resolution[tx_id]==None:
                        amount = tx_id_amount_lookup[tx_id]
                        disputed_resolution[tx_id] = "resolve"
                        held -= amount
                        available += amount
                        total = available + held
                        clients[client] = {"client": client, "total" : total, \
                           "available": available, "held": held, "locked": locked}
                        assert(total == available + held)
                elif trans_type == "chargeback":
                    if tx_id in tx_id_amount_lookup and \
                        tx_id in disputed_resolution and \
                        disputed_resolution[tx_id]==None:
                        amount = tx_id_amount_lookup[tx_id]
                        disputed_resolution[tx_id] = "chargeback"
                        available += amount
                        held -= amount
                        locked = "True"
                        clients[client] = {"client": client, "total" : total, \
                           "available": available, "held": held, "locked": locked}
                        assert(total == available + held)
                assert(total == available + held)
        return clients

    def process_disputes(self, clients, disputes_by_clients, deposits_withdrawals_by_clients):
        for client_id in disputes_by_clients:
            for disputed_tx_id in disputes_by_clients[client_id]:
                if disputed_tx_id in deposits_withdrawals_by_clients[client_id] and \
                        deposits_withdrawals_by_clients[client_id][disputed_tx_id]["type"] == "deposit":
                    #TODO need to lookup amount
                    clients[client_id]["available"] -= deposits_withdrawals_by_clients[client_id][disputed_tx_id]['amount']
                    clients[client_id]["held"]      += deposits_withdrawals_by_clients[client_id][disputed_tx_id]['amount']
        return clients

def main():
    path_to_file = sys.argv[1]
    transaction_engine = TransactionEngine(write_on_update=False)
    transaction_engine.extract_transactions_by_client(path_to_file)
    transaction_engine.process_transactions()
    print(transaction_engine.transactions_by_clients)
    print("====")
    print(transaction_engine.clients_accounts)

if __name__ == '__main__':
    main()

