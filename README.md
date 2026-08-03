# License Management System

A small desktop app for tracking software license keys, expiration dates,
and notification emails. Built with Python, SQLite, and a
[CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) GUI, with
optional Gmail integration (via the Gmail API) for sending expiry-warning
emails.

## Features

- Add and store license records (name, key, expiration date, notification email) in a local SQLite database.
- Export all stored licenses to a CSV report (`reports/license_report.csv`).
- Send an expiry-warning email (via the Gmail API) for any license expiring within 30 days.
- Zero manual database setup — the schema is created automatically on first run.

## Tech stack

- Python 3
- SQLite (via `sqlite3`, no server required)
- CustomTkinter for the GUI
- Google Gmail API (OAuth2, `google-auth` / `google-api-python-client`) for email notifications

## Getting started

### 1. Clone and install dependencies

```bash
git clone https://github.com/Lincalibur/License-Management-System.git
cd License-Management-System
pip install -r requirements.txt
```

### 2. Try it immediately with demo data (optional)

```bash
python seed_demo_data.py
python run.py
```

This seeds a few fake demo licenses so you have something to look at right away.

### 3. Run it for real

```bash
python run.py
```

The SQLite database (`license_management.db`) is created automatically in
the repo root on first launch — no setup required for adding licenses and
exporting CSV reports.

### 4. (Optional) Set up email notifications

Sending expiry-warning emails uses the Gmail API and requires your own
OAuth client credentials — none are bundled with this repo:

1. Create a project in the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Gmail API** for that project.
3. Under **Credentials**, create an **OAuth client ID** of type **Desktop app**.
4. Download the resulting JSON and save it as `credentials.json` in the repo root
   (this filename/location is the default — see below to customize).
5. Click **Send Expiry Notifications** in the app. The first run opens a
   browser window to authorize your Google account; a `token.pickle` is then
   cached locally so you don't need to re-authorize every time.

Both `credentials.json` and `token.pickle` are gitignored and must never be
committed — they grant send-as-you access to the Gmail account that
authorizes them.

If `credentials.json` is missing, the app shows a clear error explaining what
to do instead of crashing.

### Configuration

All file locations default to sensible paths in the repo root, but can be
overridden with environment variables if you'd rather keep them elsewhere:

| Variable               | Default                          | Purpose                          |
|------------------------|-----------------------------------|-----------------------------------|
| `LMS_DB_PATH`          | `<repo>/license_management.db`   | SQLite database file             |
| `LMS_CREDENTIALS_PATH` | `<repo>/credentials.json`        | Google OAuth client secret       |
| `LMS_TOKEN_PATH`       | `<repo>/token.pickle`            | Cached Google OAuth token        |
| `LMS_REPORTS_DIR`      | `<repo>/reports`                 | Where CSV reports are written    |

## Project structure

```
run.py                        # entry point (python run.py)
seed_demo_data.py             # optional demo data seeder
src/Core/
  license_management_gui.py   # CustomTkinter GUI
  license_management_db.py    # SQLite access + CSV export
  license_management_backend.py  # Gmail OAuth + expiry notification logic
  config.py                   # configurable file paths
reports/
  license_report.csv          # example CSV output
```

## License

MIT — see [LICENSE](LICENSE).
