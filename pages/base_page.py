from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import logging


class BasePage:
    """Base page class that contains common functionality for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        # Set up logging for this page
        self.logger = logging.getLogger(self.__class__.__name__)
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('[%(name)s] %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def find_element(self, by, value):
        """Find element with explicit wait"""
        return self.wait.until(EC.presence_of_element_located((by, value)))
    
    def find_elements(self, by, value):
        """Find elements with explicit wait"""
        return self.wait.until(EC.presence_of_all_elements_located((by, value)))
    
    def click_element(self, by, value):
        """Click element with explicit wait"""
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        element.click()
    
    def send_keys_to_element(self, by, value, text):
        """Send keys to element with explicit wait"""
        element = self.wait.until(EC.presence_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)
    
    def get_current_url(self):
        """Get current URL"""
        return self.driver.current_url
    
    def wait_for_url_change(self, old_url, timeout=10):
        """Wait for URL to change from old_url"""
        try:
            self.wait.until(lambda driver: driver.current_url != old_url)
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, by, value, timeout=5):
        """Check if element is present within timeout"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def log_action(self, action_description):
        """Log an action being performed"""
        self.logger.info(f"🔄 {action_description}")
    
    def log_success(self, success_message):
        """Log a successful action"""
        self.logger.info(f"✅ {success_message}")
    
    def log_page_load(self, page_name):
        """Log that a page has loaded"""
        current_url = self.get_current_url()
        self.logger.info(f"📄 {page_name} loaded - URL: {current_url}")
    
    def assert_on_page(self, expected_url_part, page_name):
        """Assert that we are on the expected page"""
        current_url = self.get_current_url()
        self.log_action(f"Verifying we are on {page_name}")
        assert expected_url_part in current_url, f"Expected to be on {page_name} (URL should contain '{expected_url_part}'), but current URL is: {current_url}"
        self.log_success(f"Successfully verified we are on {page_name}")
        return True
    
    def assert_element_present(self, by, value, element_description):
        """Assert that an element is present on the page"""
        self.log_action(f"Checking for presence of {element_description}")
        is_present = self.is_element_present(by, value)
        assert is_present, f"Expected element '{element_description}' to be present, but it was not found"
        self.log_success(f"{element_description} is present on the page")
        return True
