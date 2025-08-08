#!/usr/bin/env python3
"""Simple script to verify URL configuration is working correctly"""

from config.test_config import LOGIN_URL, BASE_URL
from pages.login_page import LoginPage
from utils.driver_manager import DriverManager

def test_url_configuration():
    """Test that page objects are using the correct URL from configuration"""
    print(f"Config BASE_URL: {BASE_URL}")
    print(f"Config LOGIN_URL: {LOGIN_URL}")
    
    # Create driver and login page
    driver = DriverManager.get_chrome_driver()
    login_page = LoginPage(driver)
    
    print(f"LoginPage URL: {login_page.url}")
    
    # Verify URLs match
    assert login_page.url == LOGIN_URL, f"LoginPage URL ({login_page.url}) doesn't match config ({LOGIN_URL})"
    
    print("✅ URL configuration is working correctly!")
    
    # Clean up
    DriverManager.quit_driver(driver)

if __name__ == "__main__":
    test_url_configuration()
