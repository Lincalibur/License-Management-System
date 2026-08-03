import csv
import os
import sqlite3
from datetime import datetime

from config import DB_PATH, REPORTS_DIR


def create_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    # Create licenses table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS licenses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        key TEXT NOT NULL,
                        expiration_date TEXT NOT NULL,
                        email TEXT NOT NULL)''')

    conn.commit()
    conn.close()


def add_license(name, key, expiration_date, email):
    if not name or not key or not expiration_date or not email:
        return "Invalid input. Please fill out all fields."

    try:
        datetime.strptime(expiration_date, "%Y-%m-%d")
    except ValueError:
        return "Invalid expiration date. Please use YYYY-MM-DD."

    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO licenses (name, key, expiration_date, email) VALUES (?, ?, ?, ?)",
                   (name, key, expiration_date, email))

    conn.commit()
    conn.close()
    return "OK"


def fetch_all_licenses():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM licenses")
    licenses = cursor.fetchall()

    conn.close()
    return licenses


def get_license_by_id(license_id):
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM licenses WHERE id=?", (license_id,))
    license = cursor.fetchone()

    conn.close()
    return license


def export_licenses_csv(filename="license_report.csv"):
    """Write all licenses to a CSV file in REPORTS_DIR and return the full path."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = os.path.join(REPORTS_DIR, filename)

    licenses = fetch_all_licenses()

    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Name", "Key", "Expiration Date", "Email"])
        writer.writerows(licenses)

    return path
