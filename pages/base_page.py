from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


class BasePage:
    """Base page class that contains common functionality for all page objects"""
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
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
