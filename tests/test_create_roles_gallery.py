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

class TestCreateRolesGallery:
    def setup_method(self, method):
        self.driver: WebDriver = DriverManager.get_chrome_driver(enable_performance_logging=True)

    def teardown_method(self, method):
        DriverManager.quit_driver(self.driver)

    def test_create_roles_gallery(self):
        test_logger = logging.getLogger("TestCreateRolesGallery")
        test_logger.info("🚀 Starting create roles gallery test")

        (
            LoginPage(self.driver)
            .login_as_valid_user()
            .go_to_company_x()
            .click_roles_table()
            .click_create_view_div()
            .click_gallery_view_option()
            .click_create_view_button()
        )

        test_logger.info("🎉 Test completed successfully!")

if __name__ == "__main__":
    test_class = TestCreateRolesGallery()
    test_class.setup_method(None)
    try:
        test_class.test_create_roles_gallery()
    finally:
        test_class.teardown_method(None)
