import requests

class BalanceManager:
    def __init__(self, api_url):
        self.api_url = api_url

    def check_balance(self, username):
        response = requests.get(f"{self.api_url}/users/{username}/balance/")
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to get balance: {response.json().get('detail', 'Unknown error')}")

    def deduct_balance(self, username, chat_id, amount):
        response = requests.put(
            f"{self.api_url}/users/{username}/balance/deduct",
            json={"chat_id": chat_id, "amount": -amount}
        )
        if response.status_code == 200:
            return response.json()
        else:
            raise ValueError(f"Failed to deduct balance: {response.json().get('detail', 'Unknown error')}")

# Example usage:
if __name__ == "__main__":
    bm = BalanceManager("http://localhost:5101")  # Adjust if needed for your environment
    try:
        balance = bm.check_balance("john_doe")
        print("Current balance:", balance)

        result = bm.deduct_balance("john_doe", "chat_12345", 10.0)
        print("New balance after deduction:", result)

    except ValueError as e:
        print(e)
