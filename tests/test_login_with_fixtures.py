import pytest
from config.test_config import TEST_EMAIL, TEST_PASSWORD


class TestNocoDBLoginWithFixtures:
    """Test class demonstrating the use of shared fixtures"""
    
    def test_login_functionality(self, login_page, dashboard_page):
        """Test login functionality using shared fixtures"""
        # Navigate to login page
        login_page.navigate_to()
        
        # Perform login
        login_page.login(TEST_EMAIL, TEST_PASSWORD)
        
        # Wait for login completion and verify redirect
        assert login_page.wait_for_login_completion(), "Login did not complete successfully"
        
        # Verify we're on dashboard page
        assert dashboard_page.is_dashboard_page(), "Not redirected to dashboard page"
    
    def test_dashboard_navigation(self, logged_in_driver, dashboard_page):
        """Test dashboard navigation using pre-logged-in driver"""
        # Wait for dashboard to load
        assert dashboard_page.wait_for_dashboard_load(), "Dashboard did not load properly"
        
        # Navigate to test_base
        assert dashboard_page.navigate_to_test_base(), "Failed to navigate to test_base"
    
    def test_login_page_elements(self, login_page):
        """Test that login page elements are present"""
        login_page.navigate_to()
        
        # Verify login page elements are present
        assert login_page.is_element_present(*login_page.EMAIL_INPUT), "Email input not found"
        assert login_page.is_element_present(*login_page.PASSWORD_INPUT), "Password input not found"
        assert login_page.is_element_present(*login_page.LOGIN_BUTTON), "Login button not found"
        
        # Verify we're on login page
        assert login_page.is_login_page(), "Not on login page"
