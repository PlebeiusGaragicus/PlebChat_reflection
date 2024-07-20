import time
import json
import requests
from pymongo import MongoClient, errors
import bolt11

from src.common import get

TOKENS_PER_SAT = 30

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')  # Replace with your actual connection string
db = client.mydatabase
invoices_collection = db.invoices
users_collection = db.users  # Assuming a collection for user balances

def check_and_manage_invoice(user_uuid):
    """
    Manages the invoice and balance process for a user.
    """
    # Check for a stored pending invoice for the given user
    invoice = invoices_collection.find_one({"user": user_uuid, "status": "pending"})
    
    if invoice is None:
        # No pending invoice found, create a new one
        new_invoice = create_invoice(user_uuid)
        new_invoice["status"] = "pending"
        invoices_collection.insert_one(new_invoice)
        present_invoice_to_user(new_invoice)
    
    else:
        # Pending invoice found, check its status
        if check_invoice_paid(invoice):
            # Invoice is paid, update user balance and mark invoice as paid atomically
            with client.start_session() as session:
                with session.start_transaction():
                    try:
                        update_invoice_status(invoice["_id"], "paid", session)
                        update_user_balance(user_uuid, invoice["amount"], session)
                        session.commit_transaction()
                    except Exception as e:
                        session.abort_transaction()
                        raise e  # Ensure the exception is raised after aborting the transaction

        elif invoice_is_expired(invoice):
            # Invoice is expired, archive it and create a new one
            invoices_collection.update_one(
                {"_id": invoice["_id"]},
                {"$set": {"status": "archived"}}
            )
            new_invoice = create_invoice(user_uuid)
            new_invoice["status"] = "pending"
            invoices_collection.insert_one(new_invoice)
            present_invoice_to_user(new_invoice)
        
        else:
            # Invoice is not paid and not expired, check remaining time
            if invoice_time_remaining(invoice) < 1800:  # Check if less than 30 minutes remaining
                # Less than 30 minutes remaining, archive it and create a new one
                invoices_collection.update_one(
                    {"_id": invoice["_id"]},
                    {"$set": {"status": "archived"}}
                )
                new_invoice = create_invoice(user_uuid)
                new_invoice["status"] = "pending"
                invoices_collection.insert_one(new_invoice)
                present_invoice_to_user(new_invoice)
            else:
                # More than 30 minutes remaining, present the existing pending invoice
                present_invoice_to_user(invoice)


def create_invoice(user_uuid, sats: int = 100):
    """
    Generates a new invoice via LNURL API and returns the invoice data.
    """
    ln_address = "turkeybiscuit@getalby.com"
    url = "https://api.getalby.com/lnurl/generate-invoice"
    params = {
        "ln": ln_address,
        "amount": sats * 1000,  # in millisats
        "comment": f"Purchased {sats * TOKENS_PER_SAT} tokens"
    }

    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        invoice_data = response.json()['invoice']
        invoice_data['user'] = user_uuid
        invoice_data['amount'] = sats  # Store the amount in satoshis
        invoice_data['created_at'] = time.time()
        return invoice_data
    else:
        raise Exception(f"Failed to create invoice: {response.status_code} {response.text}")

def check_invoice_paid(invoice):
    """
    Verifies if the invoice has been paid.
    """
    verify_url = invoice['verify']
    response = requests.get(verify_url)

    if response.status_code == 200:
        return response.json()['settled']
    else:
        raise Exception(f"Error verifying invoice status: {response.status_code} {response.text}")

def update_invoice_status(invoice_id, status, session):
    """
    Updates the status of an invoice in MongoDB.
    """
    invoices_collection.update_one(
        {"_id": invoice_id},
        {"$set": {"status": status}},
        session=session
    )

def update_user_balance(user_uuid, amount, session):
    """
    Updates the user's balance in MongoDB.
    """
    users_collection.update_one(
        {"user_uuid": user_uuid},
        {"$inc": {"balance": amount}},
        session=session
    )

def invoice_is_expired(invoice):
    """
    Checks if the invoice has expired.
    """
    now = int(time.time())
    pr = invoice['pr']
    decoded_invoice = bolt11.decode(pr)
    invoice_date = decoded_invoice.date
    expiry_tag = decoded_invoice.tags.get(bolt11.models.tags.TagChar.expire_time)
    expiry_seconds = expiry_tag.data if expiry_tag else 3600  # Default to 1 hour if no expiry tag
    expiration_time = invoice_date + expiry_seconds
    return now > expiration_time

def invoice_time_remaining(invoice):
    """
    Calculates remaining time until the invoice expires.
    """
    now = int(time.time())
    pr = invoice['pr']
    decoded_invoice = bolt11.decode(pr)
    invoice_date = decoded_invoice.date
    expiry_tag = decoded_invoice.tags.get(bolt11.models.tags.TagChar.expire_time)
    expiry_seconds = expiry_tag.data if expiry_tag else 3600  # Default to 1 hour if no expiry tag
    expiration_time = invoice_date + expiry_seconds
    return expiration_time - now

def present_invoice_to_user(invoice):
    """
    Displays the invoice details to the user.
    """
    # Implement the logic to present the invoice to the user (e.g., log, print, send to front-end)
    print(f"Invoice PR: {invoice['pr']}")
    print(f"Amount: {invoice['amount']} satoshis")

def generate_invoice_via_lnurl():
    """
    Placeholder function to generate an invoice via LNURL API.
    """
    return {
        "pr": "lnbc1pvjluezpq...",  # Example payment request
        "verify_url": "https://lnurl-verify-url"  # Example verification URL
    }

def verify_invoice_status(verify_url):
    """
    Placeholder function to verify the invoice status via the verification URL.
    """
    # Mocking a response assuming the invoice is paid
    return {
        "status": "paid"  # Example response
    }
