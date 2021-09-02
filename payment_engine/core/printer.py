def print_accounts(accounts, msg=""):
    print(msg)
    for client in accounts:
        client_id = accounts[client]["client"]
        total = accounts[client]["total"]
        available = accounts[client]["available"]
        held = accounts[client]["held"]
        locked = accounts[client]["locked"]
        print(f"client = {client_id} total = {total} " +
              f"available = {available} held = {held} locked = {locked}")
    print("----")
