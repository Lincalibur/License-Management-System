"""Populate the local database with a few obviously-fake demo licenses.

Useful for trying out the app immediately after cloning, without needing
real license data on hand.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "Core"))

from license_management_db import add_license, create_tables  # noqa: E402

DEMO_LICENSES = [
    ("Demo Office Suite", "DEMO-OFFICE-0001", "2026-09-15", "demo.user@example.com"),
    ("Demo Antivirus Pro", "DEMO-AV-0002", "2026-08-20", "demo.user@example.com"),
    ("Demo Design Studio", "DEMO-DESIGN-0003", "2027-01-05", "demo.user@example.com"),
]

if __name__ == "__main__":
    create_tables()
    for name, key, expiration_date, email in DEMO_LICENSES:
        add_license(name, key, expiration_date, email)
    print(f"Seeded {len(DEMO_LICENSES)} demo licenses.")
