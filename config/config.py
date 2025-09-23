"""Configuration file for test data and settings"""
import os
from dotenv import load_dotenv

load_dotenv()

# Test credentials
TEST_EMAIL = "admin@example.com"
TEST_PASSWORD = "12341234"

# URLs - Check multiple environment variable names for CI compatibility
BASE_URL = (
    os.getenv("BASE_URL") or           # Primary env var
    os.getenv("NOCODB_URL") or         # CI environment uses this
    os.getenv("EC2_HOST") or           # EC2 host environment variable
    "http://52.18.93.49:8080/"         # Default fallback
)

# Ensure BASE_URL ends with /
if not BASE_URL.endswith('/'):
    BASE_URL = BASE_URL + '/'

LOGIN_URL = f"{BASE_URL}dashboard/"

# Timeouts
DEFAULT_TIMEOUT = 10
LONG_TIMEOUT = 15
SHORT_TIMEOUT = 5

# Test data
TEST_BASE_NAME = "company-x"
