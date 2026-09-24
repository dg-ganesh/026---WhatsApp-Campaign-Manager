"""
Project : WhatsApp Campaign Manager
Project ID : 026

Application Configuration
"""

from pathlib import Path


APP_NAME = "WhatsApp Campaign Manager"
PROJECT_ID = "026"
APP_VERSION = "0.1.0"


PROJECT_ROOT = Path(__file__).resolve().parent.parent


DATA_DIR = PROJECT_ROOT / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
SAMPLES_DIR = DATA_DIR / "samples"

LOG_DIR = PROJECT_ROOT / "logs"
ASSETS_DIR = PROJECT_ROOT / "assets"


EXECUTION_REPORT_PATH = LOG_DIR / "execution_report.txt"
APPLICATION_LOG_PATH = LOG_DIR / "application.log"


DEFAULT_ENCODING = "utf-8-sig"
CSV_DELIMITER = ","


CONTACT_NAME_FIELD = "name"
CONTACT_PHONE_FIELD = "phone_number"


# Google Contacts CSV columns.
GOOGLE_FIRST_NAME_COLUMN = "First Name"
GOOGLE_MIDDLE_NAME_COLUMN = "Middle Name"
GOOGLE_LAST_NAME_COLUMN = "Last Name"
GOOGLE_PHONE_VALUE_COLUMN = "Phone 1 - Value"


WINDOW_WIDTH = 1050
WINDOW_HEIGHT = 700

MIN_WINDOW_WIDTH = 850
MIN_WINDOW_HEIGHT = 550

CONTACT_TABLE_HEIGHT = 18


EXECUTION_REPORT_NAME = "execution_report.txt"
APPLICATION_LOG_NAME = "application.log"


REQUIRED_DIRECTORIES = (
    DATA_DIR,
    INPUT_DIR,
    OUTPUT_DIR,
    SAMPLES_DIR,
    LOG_DIR,
    ASSETS_DIR,
)


def initialize_directories() -> None:
    """Create the directories required by the application."""
    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )


__all__ = [
    "APP_NAME",
    "PROJECT_ID",
    "APP_VERSION",
    "PROJECT_ROOT",
    "DATA_DIR",
    "INPUT_DIR",
    "OUTPUT_DIR",
    "SAMPLES_DIR",
    "LOG_DIR",
    "ASSETS_DIR",
    "EXECUTION_REPORT_PATH",
    "APPLICATION_LOG_PATH",
    "DEFAULT_ENCODING",
    "CSV_DELIMITER",
    "CONTACT_NAME_FIELD",
    "CONTACT_PHONE_FIELD",
    "GOOGLE_FIRST_NAME_COLUMN",
    "GOOGLE_MIDDLE_NAME_COLUMN",
    "GOOGLE_LAST_NAME_COLUMN",
    "GOOGLE_PHONE_VALUE_COLUMN",
    "WINDOW_WIDTH",
    "WINDOW_HEIGHT",
    "MIN_WINDOW_WIDTH",
    "MIN_WINDOW_HEIGHT",
    "CONTACT_TABLE_HEIGHT",
    "EXECUTION_REPORT_NAME",
    "APPLICATION_LOG_NAME",
    "REQUIRED_DIRECTORIES",
    "initialize_directories",
]