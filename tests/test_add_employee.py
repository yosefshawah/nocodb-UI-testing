import pytest
from pages.login_page import LoginPage
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def test_fill_out_form_for_new_employee(driver):
    """Test complete user journey: login -> navigate to company-x -> fill out new employee form"""
    login_page = LoginPage(driver)
    
    # Navigate to employee form and click add-employee div
    employee_form = (
        login_page
        .login_as_valid_user()
        .go_to_company_x()
        .click_employees_table()
        .click_sidebar_view_title()
        .click_add_employee_div()  
    )
    
    employee_form.fill_form({
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@company.com',
            'salary': '85000',
            'hire_date': 'today',  # This will click the "Today" button in the calendar
            'department_id': 'IT',  # This will select from dropdown
            'role_id': 'Developer'  # This will select from dropdown
        }).submit_form()
    
     # Wait for and verify success message
    success_message = driver.wait.until(EC.presence_of_element_located((
        By.XPATH, "//div[contains(text(), 'Successfully submitted form data')]"
    )))
    assert success_message.is_displayed(), "Success message not displayed"
    assert "Successfully submitted form data" in success_message.text, "Success message text mismatch"
    