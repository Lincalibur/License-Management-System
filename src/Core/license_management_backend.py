import base64
import os
import pickle
from datetime import datetime

import google.auth
import google.auth.transport.requests
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from config import CREDENTIALS_PATH, TOKEN_PATH
from license_management_db import fetch_all_licenses

SCOPES = ['https://www.googleapis.com/auth/gmail.send']


class GoogleCredentialsMissingError(RuntimeError):
    """Raised when credentials.json has not been set up for this deployment."""


def authenticate_google():
    creds = None
    if TOKEN_PATH and os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise GoogleCredentialsMissingError(
                    f"No Google OAuth client secret found at '{CREDENTIALS_PATH}'. "
                    "Create one in the Google Cloud Console (enable the Gmail API, "
                    "create an OAuth client ID of type 'Desktop app', download it as "
                    "credentials.json) and place it at that path, or set the "
                    "LMS_CREDENTIALS_PATH environment variable. See README.md."
                )
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def send_email(subject, body, to_email):
    creds = authenticate_google()

    try:
        service = build('gmail', 'v1', credentials=creds)

        message = {
            'raw': base64.urlsafe_b64encode(
                f"To: {to_email}\r\n"
                f"Subject: {subject}\r\n"
                f"Content-Type: text/plain; charset=utf-8\r\n"
                f"Content-Transfer-Encoding: 7bit\r\n\r\n"
                f"{body}".encode("utf-8")
            ).decode("utf-8")
        }

        send_message = service.users().messages().send(userId="me", body=message).execute()
        print(f"Message sent: {send_message['id']}")
    except HttpError as error:
        print(f"An error occurred: {error}")


def get_expiring_licenses(days_before_expiration):
    """Return license rows expiring within the given number of days."""
    licenses = fetch_all_licenses()
    today = datetime.today()
    expiring = []

    for lic in licenses:
        license_id, name, key, expiration_date, email = lic
        expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%d')

        if (expiration_date_obj - today).days <= days_before_expiration:
            expiring.append(lic)

    return expiring


def notify_expiring_licenses(days_before_expiration):
    """Send an expiry-warning email for every license expiring within N days."""
    for license_id, name, key, expiration_date, email in get_expiring_licenses(days_before_expiration):
        send_email(f"License Expiry Warning: {name}", f"Your license for {name} is about to expire.", email)
