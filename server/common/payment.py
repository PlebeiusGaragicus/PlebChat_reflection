import requests


DATABASE_API_PORT = 5101
DATABASE_API_URL = f"http://localhost"


#TODO: THESE TWO SHOULD BE COMBINED INTO ONE FUNCTION!!!!!
def assure_positive_balance(lud16: str) -> bool:
    bal = _check_balance(lud16)

    if bal is None:
        return False
    else:
        return bool(bal > 0)


def check_balance(lud16):
    bal = _check_balance(lud16)

    if bal is not None:
        yield f"User: {lud16}, Balance: {bal}"
    else:
        return "Error: Unknown error" # TODO: log and track these errors!!!


def _check_balance(lud16):
    response = requests.get(f"{DATABASE_API_URL}:{DATABASE_API_PORT}/users/{lud16}/balance/")

    if response.status_code == 200:
        user_data = response.json()
        return user_data['balance']
    else:
        #TODO: TEST THIS FLOW
        raise Exception(f"Error checking balance: {response.status_code} {response.text}")
