import requests

API = "http://localhost:5101"

#TODO: This module just needs to be better... optimized at least.  Can we persist the connection?  I don't want to open/close in every node!
class BalanceManager:
    def __init__(self, api_url = API):
        self.api_url = api_url

    def check_balance(self, username):
        response = requests.post(f"{self.api_url}/balance/", json={"username": username})
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to get balance: {response.json().get('detail', 'Unknown error')}")

    def deduct_balance(self, username, chat_id, amount):
        response = requests.put(
            f"{self.api_url}/tx/",
            json={"username": username, "chat_id": chat_id, "amount": -amount}
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to deduct balance: {response.json().get('detail', 'Unknown error')}")

def deduct(lud16, chat_id, amount):
    if not lud16:
        raise ValueError("User's lud16 is not specified")

    bm = BalanceManager()
    return bm.deduct_balance(lud16, chat_id, amount)