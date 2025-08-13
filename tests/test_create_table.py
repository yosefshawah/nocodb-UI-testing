import sys
import os

# Add the project root folder to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from pages.login_page import LoginPage

class TestCreateNewTable(unittest.TestCase):

    def setUp(self):
        chrome_options = Options()
        # Optional: run headless or customize options here
        # chrome_options.add_argument("--headless")
        
        service = Service()  # Add path to chromedriver here if needed
        
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.maximize_window()
        
        # Explicit wait with 10 seconds timeout
        self.wait = WebDriverWait(self.driver, 10)

    def tearDown(self):
        self.driver.quit()

    def test_create_new_table(self):
        login_page = LoginPage(self.driver)
        
        table_name = "projects"
        
        (
            login_page
            .login_as_valid_user()
            .go_to_company_x()
            .click_create_new()
            .click_table_option()
            .wait_for_page_load()
            .enter_table_name(table_name)
            .click_create_table_button()
            .wait_for_table_in_list(table_name)
        )
        assert True
    

if __name__ == "__main__":
    test_instance = TestCreateNewTable()
    test_instance.setUp()
    try:
        test_instance.test_create_new_table()
    finally:
        test_instance.tearDown()
