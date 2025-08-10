from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage
from .employee_form import EmployeeForm


class SidebarPage(BasePage):
    """Page object for universal sidebar functionality with method chaining support"""
    
    # Locators
    SIDEBAR_BASE_BUTTON = (By.CLASS_NAME, "active-base")
    COMPANY_X_SPAN = (By.XPATH, "//span[text()='company-x']")
    EMPLOYEES_TABLE = (By.CSS_SELECTOR, '[data-testid="nc-tbl-title-employees"]')
    SIDEBAR_VIEW_TITLE = (By.CSS_SELECTOR, '[data-testid="sidebar-view-title"]')
    ADD_EMPLOYEE_DIV = (By.XPATH, "//div[contains(text(), 'add-employee')]")
    SIDEBAR_CLOSE_BUTTON = (By.CLASS_NAME, "nc-sidebar-left-toggle-icon")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def click_sidebar_base_button(self):
        """Click the sidebar base button"""
        self.click_element(*self.SIDEBAR_BASE_BUTTON)
        return self
    
    def click_company_x(self):
        """Click the company-x span element"""
        try:
            self.click_element(*self.COMPANY_X_SPAN)
            return self
        except Exception as e:
            print(f"Could not find or click 'company-x': {e}")
            return None
    
    def click_employees_table(self):
        """Click on the employees table"""
        self.click_element(*self.EMPLOYEES_TABLE)
        return self
    
    def click_sidebar_view_title(self):
        """Click on the sidebar view title"""
        self.click_element(*self.SIDEBAR_VIEW_TITLE)
        return self
    
    def click_add_employee_div(self):
        """Click the add-employee div, close sidebar, and return the employee form page"""
        self.click_element(*self.ADD_EMPLOYEE_DIV)
        # Close the sidebar to prevent it from blocking the form
        self.click_element(*self.SIDEBAR_CLOSE_BUTTON)
        return EmployeeForm(self.driver)
    

    
    def navigate_to_company_x(self):
        """Navigate to company-x by clicking sidebar and then company-x"""
        self.click_sidebar_base_button()
        return self.click_company_x()
    
    # Additional locators for table creation
    CREATE_NEW_BUTTON = (By.CSS_SELECTOR, ".nc-button.nc-home-create-new-btn.nc-home-create-new-dropdown-btn")
    DROPDOWN_MENU = (By.CSS_SELECTOR, ".ant-dropdown-menu")
    TABLE_OPTION = (By.CSS_SELECTOR, "[data-testid='nc-sidebar-base-import']")
    
    def go_to_company_x(self):
        """Navigate to company-x base only"""
        self.wait_for_sidebar_load()
        self.navigate_to_company_x()
        return self
        
    def click_create_new(self):
        """Click the Create New button and wait for dropdown"""
        # Wait for and click the create new button
        create_new_btn = self.wait.until(EC.element_to_be_clickable(self.CREATE_NEW_BUTTON))
        assert create_new_btn.is_displayed(), "Create New button is not visible"
        create_new_btn.click()
        
        # Wait for dropdown menu to appear and verify it's visible
        dropdown = self.wait.until(EC.visibility_of_element_located(self.DROPDOWN_MENU))
        assert dropdown.is_displayed(), "Dropdown menu did not appear after clicking Create New"
        return self
        
    def click_table_option(self):
        """Click the Table option from the dropdown and return TablePage"""
        # Wait for and click the table option
        table_option = self.wait.until(EC.element_to_be_clickable(self.TABLE_OPTION))
        assert table_option.is_displayed(), "Table option is not visible in dropdown"
        table_option.click()
        
        # Return TablePage to handle the table creation form
        from .table_page import TablePage
        return TablePage(self.driver)
    
    def go_to_employees_table(self):
        """Navigate to company-x and then click employees table"""
        self.go_to_company_x()
        self.click_employees_table()
        return self
    
  
    
    def wait_for_sidebar_load(self):
        """Wait for sidebar to load completely"""
        success = self.is_element_present(*self.SIDEBAR_BASE_BUTTON, timeout=10)
        return self if success else None
