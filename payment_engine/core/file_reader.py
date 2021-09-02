import os
import csv


class FileReader():
    @staticmethod
    def readfile(path_to_file):
        transactions_by_clients = {}
        file_body_extension_tup = os.path.splitext(path_to_file)
        if file_body_extension_tup[1] == ".csv":
            with open(path_to_file) as csvfile:
                reader = csv.DictReader(csvfile)
                rows = [{k.strip(): v.strip() for k, v in row.items()}
                        for row in reader]
                for row in rows:
                    trans_type = row['type']
                    tx = row['tx']
                    client_id = row['client']
                    try:
                        amount = float(row['amount'])
                    except ValueError:
                        amount = 0
                    if client_id not in transactions_by_clients:
                        transactions_by_clients[client_id] = []
                    transactions_by_clients[client_id].append({'tx': tx,
                                                               'type': trans_type,
                                                               'amount': amount})
                return transactions_by_clients
        else:
            raise(Exception("FILE NOT SUPPORTED, CSV ONLY"))
