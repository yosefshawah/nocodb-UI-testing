from selenium.webdriver.common.by import By
from .base_page import BasePage
from config.test_config import LOGIN_URL


class LoginPage(BasePage):
    """Page object for the NocoDB login page"""
    
    # Locators
    EMAIL_INPUT = (By.XPATH, '//input[@placeholder="Enter your work email"]')
    PASSWORD_INPUT = (By.XPATH, '//input[@placeholder="Enter your password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-testid="nc-form-signin__submit"]')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = LOGIN_URL
    
    def navigate_to(self):
        """Navigate to the login page"""
        self.driver.get(self.url)
    
    def enter_email(self, email):
        """Enter email in the email input field"""
        self.send_keys_to_element(*self.EMAIL_INPUT, email)
    
    def enter_password(self, password):
        """Enter password in the password input field"""
        self.send_keys_to_element(*self.PASSWORD_INPUT, password)
    
    def click_login_button(self):
        """Click the login button"""
        self.click_element(*self.LOGIN_BUTTON)
    
    def login(self, email, password):
        """Complete login process with email and password"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
    
    def is_login_page(self):
        """Check if we're on the login page"""
        current_url = self.get_current_url()
        return "dashboard" in current_url and ("signin" in current_url or "login" in current_url)
    
    def wait_for_login_completion(self):
        """Wait for login to complete and redirect to dashboard"""
        old_url = self.get_current_url()
        return self.wait_for_url_change(old_url, timeout=15)
