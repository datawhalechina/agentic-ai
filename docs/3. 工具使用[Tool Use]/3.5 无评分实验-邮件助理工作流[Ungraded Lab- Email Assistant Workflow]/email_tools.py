from dotenv import load_dotenv
import requests
import os

load_dotenv()

BASE_URL = os.getenv("M3_EMAIL_SERVER_API_URL")

def list_all_emails() -> list:
    """
    Fetch all emails stored in the system, ordered from newest to oldest.

    Returns:
        List[dict]: A list of all emails including read and unread, 
        each represented as a dictionary with keys:
        - id
        - sender
        - recipient
        - subject
        - body
        - timestamp
        - read (boolean)
    """
    return requests.get(f"{BASE_URL}/emails").json()


def list_unread_emails() -> list:
    """
    Fetch all unread emails only.

    Returns:
        List[dict]: A list of unread emails (where `read == False`), 
        ordered from newest to oldest. Same structure as `list_all_emails`.
    """
    return requests.get(f"{BASE_URL}/emails/unread").json()


def search_emails(query: str) -> list:
    """
    Search emails containing the query in subject, body, or sender.

    Args:
        query (str): A keyword or phrase to search for.

    Returns:
        List[dict]: A list of emails matching the query string.
    """
    return requests.get(f"{BASE_URL}/emails/search", params={"q": query}).json()


def filter_emails(recipient: str = None, date_from: str = None, date_to: str = None) -> list:
    """
    Filter emails based on recipient and/or a date range.

    Args:
        recipient (str): Email address to filter by (optional).
        date_from (str): Start date in 'YYYY-MM-DD' format (optional).
        date_to (str): End date in 'YYYY-MM-DD' format (optional).

    Returns:
        List[dict]: A list of emails matching the given filters.
    """
    params = {}
    if recipient:
        params["recipient"] = recipient
    if date_from:
        params["date_from"] = date_from
    if date_to:
        params["date_to"] = date_to

    return requests.get(f"{BASE_URL}/emails/filter", params=params).json()


def get_email(email_id: int) -> dict:
    """
    Retrieve a specific email by its ID.

    Args:
        email_id (int): The unique ID of the email to fetch.

    Returns:
        dict: A single email record if found, else raises HTTP 404.
    """
    return requests.get(f"{BASE_URL}/emails/{email_id}").json()


def mark_email_as_read(email_id: int) -> dict:
    """
    Mark a specific email as read.

    Args:
        email_id (int): The ID of the email to mark as read.

    Returns:
        dict: The updated email record with `read: true`.
    """
    return requests.patch(f"{BASE_URL}/emails/{email_id}/read").json()


def mark_email_as_unread(email_id: int) -> dict:
    """
    Mark a specific email as unread.

    Args:
        email_id (int): The ID of the email to mark as unread.

    Returns:
        dict: The updated email record with `read: false`.
    """
    return requests.patch(f"{BASE_URL}/emails/{email_id}/unread").json()


def send_email(recipient: str, subject: str, body: str) -> dict:
    """
    Send an email (simulated). The sender is set automatically by the server.

    Args:
        recipient (str): The email address of the recipient.
        subject (str): The subject of the email.
        body (str): The message body content.

    Returns:
        dict: The created email record.
    """
    payload = {
        "recipient": recipient,
        "subject": subject,
        "body": body
    }
    return requests.post(f"{BASE_URL}/send", json=payload).json()


def delete_email(email_id: int) -> dict:
    """
    Delete an email by its ID.

    Args:
        email_id (int): The ID of the email to delete.

    Returns:
        dict: A confirmation message: {"message": "Email deleted"}
    """
    return requests.delete(f"{BASE_URL}/emails/{email_id}").json()


def search_unread_from_sender(sender: str) -> list:
    """
    Return all unread emails from a specific sender (case-insensitive match).

    Args:
        sender (str): The email address of the sender to search for.

    Returns:
        List[dict]: A list of unread emails where the sender matches the given address.
    """
    unread = list_unread_emails()
    return [e for e in unread if e['sender'].lower() == sender.lower()]
