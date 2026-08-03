"""Entry point: launches the License Management System GUI.

Kept at the repo root so the app can be started with `python run.py` without
needing to install the project as a package.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "src", "Core"))

from license_management_gui import main  # noqa: E402

if __name__ == "__main__":
    main()
