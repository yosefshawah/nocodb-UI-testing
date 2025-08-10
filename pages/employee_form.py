from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


class EmployeeForm(BasePage):
    """Page object for the employee form that appears after clicking add-employee"""
    
    def __init__(self, driver):
        """Initialize the employee form page and wait for it to load"""
        super().__init__(driver)
    
    def enter_field_value(self, field_name, value):
        """Enter value in any form field using its field name"""
        if field_name in ['hire_date', 'department_id', 'role_id']:
            return self.handle_special_field(field_name, value)
        
        # Regular input field
        field_locator = (By.XPATH, f"//body//div[@data-testid='nc-form-input-{field_name}']//input[contains(@class, 'nc-cell-field')]")
        self.wait.until(EC.element_to_be_clickable(field_locator)).send_keys(value)
        return self
        
    def handle_special_field(self, field_name, value):
        """Handle special interactive fields like date pickers and dropdowns"""
        if field_name == 'hire_date':
            # Click the date field to open calendar
            date_field = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, f"//body//div[@data-testid='nc-form-input-{field_name}']//input"
            )))
            date_field.click()
            
            # Click the "Today" button in the calendar
            today_button = self.wait.until(EC.element_to_be_clickable((
                By.XPATH, "//span[text()='Today']"
            )))
            today_button.click()
            
        elif field_name in ['department_id', 'role_id']:
            if field_name == 'department_id':
                # First click the department field container
                dept_field = self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//div[@data-testid='nc-form-input-departments']"
                )))
                dept_field.click()
                
                # Find and focus on the search input with placeholder
                search_input = self.wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, "input[placeholder='Search records to link...']"
                )))
                search_input.click()  # Focus on the search input
                search_input.send_keys(value)  # Type "IT"
                
                # Click the link button using its specific class and data attribute
                link_button = self.wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, "button.nc-list-item-link-unlink-btn"
                )))
                link_button.click()
                
                # Wait for the selection to be confirmed
                self.wait.until(EC.invisibility_of_element_located((
                    By.CSS_SELECTOR, "div.ant-dropdown-content"
                )))
            elif field_name == 'role_id':
                # First click the role field container
                role_field = self.wait.until(EC.element_to_be_clickable((
                    By.XPATH, "//div[@data-testid='nc-form-input-roles']"
                )))
                role_field.click()
                
                # Find and focus on the search input with placeholder
                search_input = self.wait.until(EC.presence_of_element_located((
                    By.CSS_SELECTOR, "input[placeholder='Search records to link...']"
                )))
                search_input.click()  # Focus on the search input
                search_input.send_keys(value)  # Type "developer"
                
                # Click the link button using its specific class and data attribute
                link_button = self.wait.until(EC.element_to_be_clickable((
                    By.CSS_SELECTOR, "button.nc-list-item-link-unlink-btn"
                )))
                link_button.click()
                
                # Wait for the selection to be confirmed
                self.wait.until(EC.invisibility_of_element_located((
                    By.CSS_SELECTOR, "div.ant-dropdown-content"
                )))
            
        return self
    
    def fill_form(self, data):
        """Fill multiple form fields at once using a dictionary"""
        for field_name, value in data.items():
            self.enter_field_value(field_name, value)
            # Wait after each field to ensure it's properly filled
            if field_name in ['department_id', 'role_id']:
                # For dropdowns, wait for the dropdown content to disappear
                self.wait.until(EC.invisibility_of_element_located((
                    By.CSS_SELECTOR, "div.ant-dropdown-content"
                )))
            else:
                # For regular inputs, wait for the field to be filled
                self.wait.until(EC.presence_of_element_located((
                    By.XPATH, f"//body//div[@data-testid='nc-form-input-{field_name}']//input[contains(@class, 'nc-cell-field')]"
                )))
        return self
        
    def submit_form(self):
        """Click the submit button on the form"""
        # First ensure we're on the form
        self.wait.until(EC.presence_of_element_located((
            By.XPATH, "//body//div[contains(@class, 'ant-form')]"
        )))
        
        # Then find and click the submit button
        submit_button = self.wait.until(EC.element_to_be_clickable((
            By.CSS_SELECTOR, ".ant-form button[type='submit'], .ant-form .ant-btn-primary"
        )))
        submit_button.click()
        return self

  
