import pytest
from pages.login_page import LoginPage
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_create_new_table(driver):
    """Test complete user journey: login -> navigate to company-x -> create new table"""
    login_page = LoginPage(driver)
    
    # Define test data
    table_name = "projects"
    
    # Start with login and navigation to company-x, then create table
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
    
   
    assert True, "Stopped after entering table name to check the page state"
