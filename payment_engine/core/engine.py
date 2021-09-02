import csv
from .file_reader import FileReader
from .printer import print_accounts
from .engine_exceptions import UnknownTypeException


class TotalsHelper():
    def __init__(self):
        self.disputed_resolution = {}
        self.clients = {}


class PaymentEngine():
    def __init__(self, print_on_update=False):
        self.print_on_update = print_on_update
        self.transactions_by_client = None
        self.totals_by_client = None

    def extract_transactions_by_client(self, path_to_file):
        self.transactions_by_clients = \
            self.transaction_file_reader(path_to_file)

    def process_transactions(self):
        self.clients_accounts = \
            self._process_transactions(self.transactions_by_clients)

    def update_clients_accounts_file(self, clients_accounts):
        with open("clients_accounts.csv", "w") as csvfile:
            fieldnames = ['client', 'available', 'held', 'total', 'locked']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for client in clients_accounts:
                row = clients_accounts[client]
                writer.writerow(row)

    def transaction_file_reader(self, path_to_file):
        return FileReader.readfile(path_to_file)

    def _deposits_logic(self, client, tx_id, transaction, totals):
        if tx_id not in totals.processed_transactions:
            totals.tx_id_amount_lookup[tx_id] = transaction["amount"]
            totals.clients[client]["available"] += transaction["amount"]
            totals.clients[client]["total"] += transaction["amount"]
            totals.processed_transactions[tx_id] = "deposit"
            assert(totals.clients[client]["total"] ==
                   totals.clients[client]["available"] +
                   totals.clients[client]["held"])

    def _withdrawals_logic(self, client, tx_id, transaction, totals):
        if tx_id not in totals.processed_transactions:
            totals.tx_id_amount_lookup[tx_id] = transaction["amount"]
            amount = transaction["amount"]
            if amount <= totals.clients[client]["available"]:
                totals.clients[client]["total"] -= transaction["amount"]
                totals.clients[client]["available"] -= transaction["amount"]
                totals.processed_transactions[tx_id] = "withdrawal"
                assert(totals.clients[client]["total"] ==
                       totals.clients[client]["available"] +
                       totals.clients[client]["held"])

    def _disputes_logic(self, client, tx_id, totals):
        if tx_id in totals.tx_id_amount_lookup and \
                totals.processed_transactions[tx_id] == "deposit" and \
                tx_id not in totals.disputed_resolution:
            amount = totals.tx_id_amount_lookup[tx_id]
            totals.clients[client]["available"] -= amount
            totals.clients[client]["held"] += amount
            totals.clients[client]["total"] = \
                totals.clients[client]["available"] + \
                totals.clients[client]["held"]
            totals.disputed_resolution[tx_id] = None
            assert(totals.clients[client]["total"] ==
                   totals.clients[client]["available"] +
                   totals.clients[client]["held"])

    def _resolves_logic(self, client, tx_id, transaction, totals):
        if tx_id in totals.tx_id_amount_lookup and \
            tx_id in totals.disputed_resolution and \
                totals.disputed_resolution[tx_id] is None:
            amount = totals.tx_id_amount_lookup[tx_id]
            totals.disputed_resolution[tx_id] = "resolve"
            totals.clients[client]["held"] -= amount
            totals.clients[client]["available"] += amount
            totals.clients[client]["total"] = \
                totals.clients[client]["available"] + \
                totals.clients[client]["held"]
            assert(totals.clients[client]["total"] ==
                   totals.clients[client]["available"] +
                   totals.clients[client]["held"])

    def _chargeback_logic(self, client, tx_id, transaction, totals):
        if tx_id in totals.tx_id_amount_lookup and \
            tx_id in totals.disputed_resolution and \
                totals.disputed_resolution[tx_id] is None:
            amount = totals.tx_id_amount_lookup[tx_id]
            totals.disputed_resolution[tx_id] = "chargeback"
            totals.clients[client]["held"] -= amount
            totals.clients[client]["locked"] = "true"
            totals.clients[client]["total"] = \
                totals.clients[client]["available"] + \
                totals.clients[client]["held"]
            assert(totals.clients[client]["total"] ==
                   totals.clients[client]["available"] +
                   totals.clients[client]["held"])

    def _process_transactions(self, transactions_by_clients):
        totals = TotalsHelper()
        totals.processed_transactions = {}
        for client in transactions_by_clients:
            totals.tx_id_amount_lookup = {}
            totals.locked = 'false'
            totals.clients[client] = {"client": client,
                                      "available": 0.0,
                                      "held": 0.0,
                                      "total": 0.0,
                                      "locked": "false"}
            for transaction in transactions_by_clients[client]:
                trans_type = transaction['type']
                if trans_type not in ["deposit", "withdrawal",
                                      "dispute", "resolve", "chargeback"]:
                    raise UnknownTypeException(f"{trans_type} is not supported")
                tx_id = transaction['tx']
                if totals.clients[client]["locked"] == "true":
                    is_locked = True
                else:
                    is_locked = False
                if trans_type == "deposit" and not is_locked:
                    self._deposits_logic(client, tx_id, transaction, totals)
                    if self.print_on_update:
                        print_accounts(totals.clients,
                                       "processing deposit = " +
                                       f"{transaction['amount']}" +
                                       f"for client = {client}")
                elif trans_type == "withdrawal" and not is_locked:
                    self._withdrawals_logic(client, tx_id, transaction, totals)
                    if self.print_on_update:
                        print_accounts(totals.clients,
                                       "processing withdrawal = " +
                                       f"{transaction['amount']}" +
                                       f"for client = {client}")
                elif trans_type == "dispute" and not is_locked:
                    self._disputes_logic(client, tx_id, totals)
                    if self.print_on_update:
                        print_accounts(totals.clients,
                                       "processing dispute for client = " +
                                       f"{client}")
                elif trans_type == "resolve" and not is_locked:
                    self._resolves_logic(client, tx_id, transaction, totals)
                    if self.print_on_update:
                        print_accounts(totals.clients,
                                       "processing resolve for client = " +
                                       f"{client}")
                elif trans_type == "chargeback" and not is_locked:
                    self._chargeback_logic(client, tx_id, transaction, totals)
                    if self.print_on_update:
                        print_accounts(totals.clients,
                                       "processing chargeback for client = " +
                                       f"{client}")
                assert(totals.clients[client]["total"] ==
                       totals.clients[client]["available"] +
                       totals.clients[client]["held"])
        return totals.clients
