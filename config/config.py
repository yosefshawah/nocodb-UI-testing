"""Configuration file for test data and settings"""
import os
from dotenv import load_dotenv

load_dotenv()

# Test credentials
TEST_EMAIL = "admin@example.com"
TEST_PASSWORD = "12341234"

# URLs
BASE_URL = "http://52.18.93.49:8080/"
BASE_URL = os.getenv("BASE_URL")
LOGIN_URL = f"{BASE_URL}dashboard/"

# Timeouts
DEFAULT_TIMEOUT = 10
LONG_TIMEOUT = 15
SHORT_TIMEOUT = 5

# Test data
TEST_BASE_NAME = "company-x"
