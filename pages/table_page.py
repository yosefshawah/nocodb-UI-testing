from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage

class TablePage(BasePage):
    """Page object for table creation and management with method chaining support"""
    
    # Locators
    TABLE_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Enter table name']")
    CREATE_TABLE_BUTTON = (By.CSS_SELECTOR, ".ant-modal-body button.ant-btn-primary")
    
    def __init__(self, driver):
        """Initialize the table page"""
        super().__init__(driver)
    
    def wait_for_page_load(self):
        """Wait for the table creation modal to be present and verify its state"""
        # Wait for modal wrapper to be present and visible
        modal = self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".ant-modal-wrap.nc-modal-wrapper"
        )))
        assert modal.is_displayed(), "Table creation modal is not visible"
        return self
    
    def enter_table_name(self, name):
        """Enter the table name in the input field
        Args:
            name (str): The name to give to the table
        """
        # Enter the table name
        table_name_field = self.wait.until(EC.element_to_be_clickable(self.TABLE_NAME_INPUT))
        table_name_field.clear()
        table_name_field.send_keys(name)
        return self
        
    def click_create_table_button(self):
        """Click the Create Table button"""
        # Wait for modal body to be present
        self.wait.until(EC.presence_of_element_located((
            By.CSS_SELECTOR, ".ant-modal-body"
        )))
        
        # Find and click the create button
        create_button = self.wait.until(EC.element_to_be_clickable(self.CREATE_TABLE_BUTTON))
        create_button.click()
        return self