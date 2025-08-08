import pytest
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from utils.driver_manager import DriverManager
from config.test_config import TEST_EMAIL, TEST_PASSWORD


class TestNocoDBLogin:
    """Test class for NocoDB login functionality using Page Object Model"""
    
    @pytest.fixture(autouse=True)
    def setup_teardown(self):
        """Setup and teardown for each test"""
        self.driver = DriverManager.get_chrome_driver()
        yield
        DriverManager.quit_driver(self.driver)
    
    def test_nocodb_login_and_navigation(self):
        """Test login functionality and navigation to test_base"""
        # Initialize page objects
        login_page = LoginPage(self.driver)
        dashboard_page = DashboardPage(self.driver)
        
        # Navigate to login page
        login_page.navigate_to()
        
        # Perform login
        login_page.login(TEST_EMAIL, TEST_PASSWORD)
        
        # Wait for login completion and verify redirect
        assert login_page.wait_for_login_completion(), "Login did not complete successfully"
        
        # Verify we're on dashboard page
        assert dashboard_page.is_dashboard_page(), "Not redirected to dashboard page"
        
        # Wait for dashboard to load
        assert dashboard_page.wait_for_dashboard_load(), "Dashboard did not load properly"
        
        # Navigate to test_base
        assert dashboard_page.navigate_to_test_base(), "Failed to navigate to test_base"
    
    def test_login_page_elements(self):
        """Test that login page elements are present"""
        login_page = LoginPage(self.driver)
        login_page.navigate_to()
        
        # Verify login page elements are present
        assert login_page.is_element_present(*login_page.EMAIL_INPUT), "Email input not found"
        assert login_page.is_element_present(*login_page.PASSWORD_INPUT), "Password input not found"
        assert login_page.is_element_present(*login_page.LOGIN_BUTTON), "Login button not found"
        
        # Verify we're on login page
        assert login_page.is_login_page(), "Not on login page"
