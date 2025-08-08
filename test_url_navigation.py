#!/usr/bin/env python3
"""Test to verify browser navigation to remote URL"""

import time
from pages.login_page import LoginPage
from utils.driver_manager import DriverManager

def test_url_navigation():
    """Test that browser navigates to the remote URL"""
    driver = DriverManager.get_chrome_driver()
    login_page = LoginPage(driver)
    
    print(f"Expected URL: {login_page.url}")
    
    # Navigate to the page
    login_page.navigate_to()
    
    # Wait a moment for page to load
    time.sleep(3)
    
    # Get the actual URL
    actual_url = driver.current_url
    print(f"Actual URL: {actual_url}")
    
    # Check if we're on the remote server
    if "52.18.93.49" in actual_url:
        print("✅ Successfully navigating to remote server!")
    else:
        print("❌ Still navigating to localhost!")
    
    # Take a screenshot for debugging
    driver.save_screenshot("debug_screenshot.png")
    print("Screenshot saved as debug_screenshot.png")
    
    # Clean up
    DriverManager.quit_driver(driver)

if __name__ == "__main__":
    test_url_navigation()
