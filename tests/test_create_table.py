import sys
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

# Add the project root (one folder up from tests) to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from pages.login_page import LoginPage


class TestCreateNewTable:
    def setup_method(self, method):
        options = webdriver.ChromeOptions()
        options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver: WebDriver = webdriver.Chrome(options=options)

    def teardown_method(self, method):
        self.driver.quit()

    def _get_network_logs(self):
        logs = self.driver.get_log('performance')
        network_events = []
        for entry in logs:
            log = entry['message']
            if '"Network.responseReceived"' in log:
                network_events.append(log)
        return network_events

    def test_create_new_table(self):
        login_page = LoginPage(self.driver)
        table_name = "test-table"

        login_page.login_as_valid_user()\
            .go_to_company_x()\
            .click_create_new()\
            .click_table_option()\
            .wait_for_page_load()\
            .enter_table_name(table_name)\
            .click_create_table_button()

        # Check network logs for 200 response on /tables endpoint
        network_logs = self._get_network_logs()

        success = any('"status":200' in log and '/tables' in log for log in network_logs)

        assert success, "No successful 200 response for table creation found in network logs"


if __name__ == "__main__":
    test_class = TestCreateNewTable()
    test_class.setup_method(None)
    try:
        test_class.test_create_new_table()
        print("Test ran successfully!")
    finally:
        test_class.teardown_method(None)
