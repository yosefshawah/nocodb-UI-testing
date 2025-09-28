import sys
from pathlib import Path
import pytest
import logging
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium import webdriver

# Configure logging to show all levels
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Add the project root (one folder up from tests) to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pages.login_page import LoginPage
from utils.driver_manager import DriverManager

class TestDuplicateBase:
    def setup_method(self, method):
        self.driver: WebDriver = DriverManager.get_chrome_driver(enable_performance_logging=True)

    def teardown_method(self, method):
        DriverManager.quit_driver(self.driver)

    def test_duplicate_base(self):
        test_logger = logging.getLogger("TestDuplicateBase")
        test_logger.info("🚀 Starting base duplication test")

        sidebar_page = (
            LoginPage(self.driver)
            .login_as_valid_user()
            .click_company_x_base()
            .click_duplicate_base()
            .click_duplicate_base_button()
        )
        
if __name__ == "__main__":
    test_class = TestDuplicateBase()
    test_class.setup_method(None)
    try:
        test_class.test_duplicate_base()
    finally:
        test_class.teardown_method(None)