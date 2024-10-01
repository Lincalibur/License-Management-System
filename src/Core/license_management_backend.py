import sqlite3
from datetime import datetime, timedelta
from email_notifications import send_email_notification
import csv
import os

DATABASE_FILE = 'licenses.db'


def create_database():
    """Create the database and the licenses table if it doesn't exist."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS licenses (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            key TEXT NOT NULL,
            expiration_date DATE NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def add_license(name, key, expiration_date):
    """Add a new license to the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO licenses (name, key, expiration_date)
        VALUES (?, ?, ?)
    ''', (name, key, expiration_date))
    conn.commit()
    conn.close()


def get_all_licenses():
    """Retrieve all licenses from the database."""
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM licenses')
    licenses = cursor.fetchall()
    conn.close()
    return licenses


def check_expiring_licenses(days=30):
    """Check for licenses expiring within the given number of days."""
    threshold_date = datetime.now() + timedelta(days=days)
    conn = sqlite3.connect(DATABASE_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM licenses WHERE expiration_date <= ?
    ''', (threshold_date.strftime('%Y-%m-%d'),))
    expiring_licenses = cursor.fetchall()
    conn.close()
    return expiring_licenses


def notify_expiring_licenses(days=30, user_email="your_email@example.com"):
    """Notify user about licenses expiring soon."""
    expiring_licenses = check_expiring_licenses(days)
    
    if expiring_licenses:
        for lic in expiring_licenses:
            subject = f"License Expiration Alert: {lic[1]}"
            body = f"Your license for '{lic[1]}' will expire on {lic[3]}. Please take action to renew it."
            send_email_notification(user_email, subject, body)
    else:
        print("No licenses expiring soon.")


def generate_report(filename='reports/license_report.csv'):
    """Generate a CSV report of all licenses."""
    os.makedirs(os.path.dirname(filename), exist_ok=True)  # Create reports directory if it doesn't exist
    licenses = get_all_licenses()
    
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['ID', 'Name', 'Key', 'Expiration Date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for lic in licenses:
            writer.writerow({'ID': lic[0], 'Name': lic[1], 'Key': lic[2], 'Expiration Date': lic[3]})

    print(f"Report generated: {filename}")


# Initialize the database when the script is run
create_database()
