import requests

DATABASE_API_PORT = 5101
DATABASE_API_URL = f"http://localhost"

class UserNotRegistered(Exception):
    pass


#TODO: THESE TWO SHOULD BE COMBINED INTO ONE FUNCTION!!!!!
def assure_positive_balance(lud16: str) -> bool:
    bal = _check_balance(lud16)

    if bal is None:
        return False
    else:
        return bool(bal > 0)

def get_invoice(lud16: str, sats: int = 100):
    response = requests.get(f"{DATABASE_API_URL}:{DATABASE_API_PORT}/invoice/", json={"username": lud16, "sats": sats})

    if response.status_code == 200:
        invoice = response.json()
        if 'error' in invoice:
            raise Exception(f"Error creating invoice: {invoice['error']}")
        return invoice
    else:
        # TODO: log and track these errors!!!
        raise Exception(f"Error getting invoice: {response.status_code} {response.text}")

def show_user_balance(lud16):
    bal = _check_balance(lud16)

    if bal is not None:
        yield f"User: {lud16}, Balance: {bal}"
    else:
        return "Error: Unknown error" # TODO: log and track these errors!!!


def get_balance(lud16):
    bal = _check_balance(lud16)

    if bal is not None:
        return bal
    else:
        raise Exception("Error: error in get_balance()") # TODO: log and track these errors!!!


def _check_balance(lud16):
    # Note: Using params instead of json to send username as a query parameter
    response = requests.get(f"{DATABASE_API_URL}:{DATABASE_API_PORT}/balance/", params={"username": lud16})

    try:
        response.raise_for_status()  # Raises HTTPError for bad HTTP responses
        user_data = response.json()
        return user_data['balance']
    except requests.exceptions.HTTPError as e:
        print("*" * 80)
        print(f"Error: {e}")
        print(response.text)
        print("*" * 80)

        if response.status_code == 404 and response.json().get("detail") == "User not found":
            # raise UserNotRegistered(f"User not registered: {lud16}")
            return 0 #TODO: nope, this is a bad idea... we should raise the exception and handle it in the app.py
        else:
            # TODO: TEST THIS FLOW
            raise Exception(f"Error checking balance: {response.status_code} {response.text}")


