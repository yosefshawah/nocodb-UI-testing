from selenium.webdriver.common.by import By
from .base_page import BasePage
from config.test_config import BASE_URL


class DashboardPage(BasePage):
    """Page object for the NocoDB dashboard page"""
    
    # Locators
    SIDEBAR_BASE_BUTTON = (By.CLASS_NAME, "active-base")
    TEST_BASE_SPAN = (By.XPATH, "//span[text()='test_base']")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def is_dashboard_page(self):
        """Check if we're on the dashboard page"""
        current_url = self.get_current_url()
        return BASE_URL in current_url and "dashboard" in current_url and "signin" not in current_url
    
    def click_sidebar_base_button(self):
        """Click the sidebar base button"""
        self.click_element(*self.SIDEBAR_BASE_BUTTON)
    
    def click_test_base(self):
        """Click the test_base span element"""
        try:
            self.click_element(*self.TEST_BASE_SPAN)
            return True
        except Exception as e:
            print(f"Could not find or click 'test_base': {e}")
            return False
    
    def navigate_to_test_base(self):
        """Navigate to test_base by clicking sidebar and then test_base"""
        self.click_sidebar_base_button()
        return self.click_test_base()
    
    def wait_for_dashboard_load(self):
        """Wait for dashboard to load completely"""
        return self.is_element_present(*self.SIDEBAR_BASE_BUTTON, timeout=10)
