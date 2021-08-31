import csv

class TotalsHelper():
    pass

class PaymentEngine():
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

    def _deposits_logic(self, client, tx_id, transaction, totals):
        if tx_id not in totals.processed_transactions:
            totals.tx_id_amount_lookup[tx_id] = transaction["amount"]
            #totals.total += transaction["amount"]
            totals.available += transaction["amount"]
            totals.total += transaction["amount"]
            totals.clients[client] = {"client": client, "total" : totals.total, \
                "available": totals.available, "held": totals.held, "locked": totals.locked}
            totals.processed_transactions[tx_id] = "deposit"
            assert(totals.total == totals.available + totals.held)

    def _withdrawals_logic(self, client, tx_id, transaction, totals):
        if tx_id not in totals.processed_transactions:
            totals.tx_id_amount_lookup[tx_id] = transaction["amount"]
            amount = transaction["amount"]
            if amount <= totals.available: 
                totals.total -= transaction["amount"]
                totals.available -= transaction["amount"]
                totals.clients[client] = {"client": client, "total" : totals.total, \
                    "available": totals.available, "held": totals.held, "locked": totals.locked}
                totals.processed_transactions[tx_id] = "withdrawal"

    def _disputes_logic(self, client, tx_id, totals):
        if tx_id in totals.tx_id_amount_lookup and \
            totals.processed_transactions[tx_id] == "deposit":
            amount = totals.tx_id_amount_lookup[tx_id]
            totals.available -= amount
            totals.held += amount
            totals.disputed_resolution[tx_id] = None
            totals.total = totals.available + totals.held
            totals.clients[client] = {"client": client, "total" : totals.total, \
                "available": totals.available, "held": totals.held, "locked": totals.locked}
            assert(totals.total == totals.available + totals.held)

    def _resolves_logic(self, client, tx_id, transaction, totals):
        if tx_id in totals.tx_id_amount_lookup and \
            tx_id in totals.disputed_resolution and \
            totals.disputed_resolution[tx_id]==None:
            amount = totals.tx_id_amount_lookup[tx_id]
            totals.disputed_resolution[tx_id] = "resolve"
            totals.held -= amount
            totals.available += amount
            totals.total = totals.available + totals.held
            totals.clients[client] = {"client": client, "total" : totals.total, \
                "available": totals.available, "held": totals.held, "locked": totals.locked}
            assert(totals.total == totals.available + totals.held)

    def _chargeback_logic(self, client, tx_id, transaction, totals):
        if tx_id in totals.tx_id_amount_lookup and \
            tx_id in totals.disputed_resolution and \
            totals.disputed_resolution[tx_id]==None:
            amount = totals.tx_id_amount_lookup[tx_id]
            totals.disputed_resolution[tx_id] = "chargeback"
            #available += amount
            totals.held -= amount
            totals.locked = "true"
            totals.total = totals.available + totals.held
            totals.clients[client] = {"client": client, "total" : totals.total, \
                "available": totals.available, "held": totals.held, "locked": totals.locked}
            assert(totals.total == totals.available + totals.held)

    def _process_transactions(self, transactions_by_clients):
        totals = TotalsHelper()
        totals.disputed_resolution = {}
        totals.clients ={}
        totals.processed_transactions = {}
        for client in transactions_by_clients:
            totals.tx_id_amount_lookup = {}
            totals.total = 0.0
            totals.held = 0.0
            totals.available = 0.0
            totals.locked = 'false'
            totals.clients[client] = {"locked": "false"}
            for transaction in transactions_by_clients[client]:
                trans_type = transaction['type']
                tx_id = transaction['tx']
                if totals.clients[client]["locked"] == "true":
                    is_locked = True
                else:
                    is_locked = False
                if trans_type == "deposit" and not is_locked:
                    self._deposits_logic(client, tx_id, transaction, totals)
                    if self.write_on_update:
                        self.update_clients_accounts_file(totals.clients)
                elif trans_type == "withdrawal" and not is_locked:
                    self._withdrawals_logic(client, tx_id, transaction, totals)
                    if self.write_on_update:
                        self.update_clients_accounts_file(totals.clients)
                elif trans_type == "dispute" and not is_locked:
                    self._disputes_logic(client, tx_id, totals)
                    if self.write_on_update:
                        self.update_clients_accounts_file(totals.clients)
                elif trans_type == "resolve" and not is_locked:
                    self._resolves_logic(client, tx_id, transaction, totals)
                elif trans_type == "chargeback" and not is_locked:
                    self._chargeback_logic(client, tx_id, transaction, totals)
                assert(totals.total == totals.available + totals.held)
                
        return totals.clients
