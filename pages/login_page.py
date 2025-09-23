from selenium.webdriver.common.by import By
from .base_page import BasePage
from config.config import LOGIN_URL, TEST_EMAIL, TEST_PASSWORD


class LoginPage(BasePage):
    """Page object for the NocoDB login page with method chaining support"""
    
    # Locators
    EMAIL_INPUT = (By.XPATH, '//input[@placeholder="Enter your work email"]')
    PASSWORD_INPUT = (By.XPATH, '//input[@placeholder="Enter your password"]')
    LOGIN_BUTTON = (By.CSS_SELECTOR, '[data-testid="nc-form-signin__submit"]')
    
    def __init__(self, driver):
        super().__init__(driver)
        self.url = LOGIN_URL
    
    def navigate_to(self):
        """Navigate to the login page"""
        self.log_action(f"Navigating to login page: {self.url}")
        self.driver.get(self.url)
        self.assert_on_page("dashboard", "Login Page")
        self.assert_element_present(*self.EMAIL_INPUT, "Email input field")
        self.assert_element_present(*self.PASSWORD_INPUT, "Password input field")
        self.log_success("Successfully navigated to login page")
        return self
    
    def enter_email(self, email):
        """Enter email in the email input field"""
        self.log_action(f"Entering email: {email}")
        self.send_keys_to_element(*self.EMAIL_INPUT, email)
        self.log_success("Email entered successfully")
        return self
    
    def enter_password(self, password):
        """Enter password in the password input field"""
        self.log_action("Entering password")
        self.send_keys_to_element(*self.PASSWORD_INPUT, password)
        self.log_success("Password entered successfully")
        return self
    
    def click_login_button(self):
        """Click the login button"""
        self.log_action("Clicking login button")
        self.assert_element_present(*self.LOGIN_BUTTON, "Login button")
        self.click_element(*self.LOGIN_BUTTON)
        self.log_success("Login button clicked")
        return self
    
    def login(self, email, password):
        """Complete login process with email and password"""
        self.enter_email(email)
        self.enter_password(password)
        self.click_login_button()
        return self
    
    def login_as_valid_user(self, email=None, password=None):
        """Login as valid user and return sidebar page for chaining"""
        from .sidebar_page import SidebarPage
        
        email = email or TEST_EMAIL
        password = password or TEST_PASSWORD
        
        self.navigate_to()
        self.login(email, password)
        self.wait_for_login_completion()
        
        return SidebarPage(self.driver)
    
    def is_login_page(self):
        """Check if we're on the login page"""
        current_url = self.get_current_url()
        return "dashboard" in current_url and ("signin" in current_url or "login" in current_url)
    
    def wait_for_login_completion(self):
        """Wait for login to complete and redirect to dashboard"""
        self.log_action("Waiting for login to complete")
        old_url = self.get_current_url()
        success = self.wait_for_url_change(old_url, timeout=15)
        if success:
            self.log_success("Login completed successfully - redirected to dashboard")
            self.log_page_load("Dashboard")
        else:
            self.logger.error("Login did not complete within timeout")
        return self if success else None
