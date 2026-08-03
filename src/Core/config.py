"""Central configuration for file paths, overridable via environment variables."""
import os

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DB_PATH = os.environ.get("LMS_DB_PATH", os.path.join(_REPO_ROOT, "license_management.db"))
CREDENTIALS_PATH = os.environ.get("LMS_CREDENTIALS_PATH", os.path.join(_REPO_ROOT, "credentials.json"))
TOKEN_PATH = os.environ.get("LMS_TOKEN_PATH", os.path.join(_REPO_ROOT, "token.pickle"))
REPORTS_DIR = os.environ.get("LMS_REPORTS_DIR", os.path.join(_REPO_ROOT, "reports"))
