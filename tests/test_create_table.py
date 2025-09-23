import sys
from pathlib import Path
import pytest
import logging
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

# Configure logging to show all levels
logging.basicConfig(level=logging.INFO, format='%(message)s')


# Add the project root (one folder up from tests) to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pages.login_page import LoginPage
from utils.driver_manager import DriverManager


class TestCreateNewTable:
    def setup_method(self, method):
        # Use DriverManager for automatic CI detection and headless mode
        # Enable performance logging for network verification
        self.driver: WebDriver = DriverManager.get_chrome_driver(enable_performance_logging=True)

    def teardown_method(self, method):
        DriverManager.quit_driver(self.driver)

    def _get_network_logs(self):
        """Extract network events from browser performance logs"""
        logs = self.driver.get_log('performance')
        network_events = []
        for entry in logs:
            log = entry['message']
            if '"Network.responseReceived"' in log:
                network_events.append(log)
        return network_events

    def test_create_new_table(self):
        # Set up test logger
        test_logger = logging.getLogger("TestCreateNewTable")
        test_logger.info("🚀 Starting table creation test")
        
        login_page = LoginPage(self.driver)
        table_name = "test-table"
        test_logger.info(f"📝 Table name to create: {table_name}")

        # Execute the table creation flow with explicit waits
        test_logger.info("🔗 Executing table creation flow with method chaining")
        table_page = (
            login_page
            .login_as_valid_user()
            .go_to_company_x()
            .click_create_new()
            .click_table_option()
            .wait_for_page_load()
            .enter_table_name(table_name)
            .click_create_table_button()
        )

        # Wait a moment for network request to complete
        test_logger.info("⏳ Waiting for network request to complete")
        self.driver.implicitly_wait(2)
        
        # Check network logs for successful table creation
        test_logger.info("🔍 Checking network logs for table creation success")
        network_logs = self._get_network_logs()
        success = any('"status":200' in log and '/tables' in log for log in network_logs)
        
        if success:
            test_logger.info("✅ Table creation verified via network logs")
        else:
            test_logger.error("❌ No successful table creation response found in logs")
        
        assert success, "No successful 200 response for table creation found in network logs"
        test_logger.info("🎉 Test completed successfully!")





if __name__ == "__main__":
    test_class = TestCreateNewTable()
    test_class.setup_method(None)
    try:
        test_class.test_create_new_table()
    finally:
        test_class.teardown_method(None)
