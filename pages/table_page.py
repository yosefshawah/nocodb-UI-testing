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
    
    def wait_for_table_in_list(self, table_name):
        """Wait until the newly created table appears in the table list"""
        # Locate all table titles
        table_locator = (By.CSS_SELECTOR, ".nc-tbl-title span")
        
        # Wait until at least one span element appears
        table_elements = self.wait.until(EC.presence_of_all_elements_located(table_locator))
        
        # Find the one whose text matches the table_name
        matching_table = None
        for elem in table_elements:
            if elem.text.strip() == table_name:
                matching_table = elem
                break
        
        assert matching_table is not None, f"New table '{table_name}' not found in the list"
        return self