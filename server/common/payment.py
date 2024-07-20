import requests


DATABASE_API_PORT = 5101
DATABASE_API_URL = f"http://localhost"


def assure_positive_balance(lud16: str) -> bool:
    response = requests.get(f"{DATABASE_API_URL}:{DATABASE_API_PORT}/users/{lud16}/balance/")

    if response.status_code == 200:
        user_data = response.json()
        balance = user_data['balance']
        if balance > 0:
            return True
        else:
            return False
    else:
        return False


def cmd_bal(lud16):
    response = requests.get(f"{DATABASE_API_URL}:{DATABASE_API_PORT}/users/{lud16}/balance/")

    if response.status_code == 200:
        user_data = response.json()
        yield f"User: {user_data['username']}, Balance: {user_data['balance']}"
    else:
        yield f"Error: {response.json().get('detail', 'Unknown error')}"
