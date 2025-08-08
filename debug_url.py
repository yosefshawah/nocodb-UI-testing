#!/usr/bin/env python3
"""Debug script to check what URL is being used"""

# Import without selenium to avoid dependency issues
from config.test_config import LOGIN_URL, BASE_URL

print("=== URL Configuration Debug ===")
print(f"BASE_URL from config: {BASE_URL}")
print(f"LOGIN_URL from config: {LOGIN_URL}")

# Try to import LoginPage to see what URL it uses
try:
    from pages.login_page import LoginPage
    print("✅ LoginPage imported successfully")
    
    # Create a mock driver to test
    class MockDriver:
        def __init__(self):
            pass
    
    login_page = LoginPage(MockDriver())
    print(f"LoginPage.url: {login_page.url}")
    
    if login_page.url == LOGIN_URL:
        print("✅ LoginPage is using the correct URL from config!")
    else:
        print(f"❌ LoginPage URL ({login_page.url}) doesn't match config ({LOGIN_URL})")
        
except Exception as e:
    print(f"❌ Error importing LoginPage: {e}")
