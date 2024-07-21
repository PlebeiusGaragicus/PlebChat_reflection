import requests

API = "http://localhost:5101"

class BalanceManager:
    def __init__(self, api_url=API):
        self.api_url = api_url
        self.session = requests.Session()  # Persist the connection

    def __del__(self):
        self.session.close()  # Ensure the session is closed when the instance is destroyed

    def check_balance(self, username):
        try:
            response = self.session.get(f"{self.api_url}/balance/", params={"username": username})
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to get balance: {e}")

    def deduct_balance(self, username, chat_id, amount):
        try:
            response = self.session.put(
                f"{self.api_url}/tx/",
                json={"username": username, "chat_id": chat_id, "amount": -amount}
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Failed to deduct balance: {e}")

def deduct(lud16, chat_id, amount):
    if not lud16:
        raise ValueError("User's lud16 is not specified")

    bm = BalanceManager()
    return bm.deduct_balance(lud16, chat_id, amount)

# Example Usage:
# bm = BalanceManager()
# print(bm.check_balance("some_username"))
# print(bm.deduct_balance("some_username", "chat_id_123", 50))
