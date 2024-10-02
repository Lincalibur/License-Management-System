import pickle
import base64
import os
import google.auth
import google_auth_oauthlib.flow
import google.auth.transport.requests
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta
from license_management_db import add_license, fetch_all_licenses

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def authenticate_google():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(google.auth.transport.requests.Request())
        else:
            flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
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

def notify_expiring_licenses(days_before_expiration):
    licenses = fetch_all_licenses()
    today = datetime.today()

    for lic in licenses:
        license_id, name, key, expiration_date, email = lic
        expiration_date_obj = datetime.strptime(expiration_date, '%Y-%m-%d')
        
        # Check if the license is expiring within the specified days
        if (expiration_date_obj - today).days <= days_before_expiration:
            send_email(f"License Expiry Warning: {name}", f"Your license for {name} is about to expire.", email)
