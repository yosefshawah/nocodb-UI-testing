from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from .base_page import BasePage


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
        """Click the add-employee div, close sidebar, and stay on current page"""
        self.click_element(*self.ADD_EMPLOYEE_DIV)
        # Close the sidebar to prevent it from blocking the form
        self.click_element(*self.SIDEBAR_CLOSE_BUTTON)
        return self
    

    
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
        self.log_action("Navigating to company-x base")
        self.wait_for_sidebar_load()
        # Add explicit wait before clicking company-x
        self.wait.until(EC.element_to_be_clickable(self.COMPANY_X_SPAN))
        self.assert_element_present(*self.COMPANY_X_SPAN, "Company-X base button")
        self.navigate_to_company_x()
        self.log_success("Successfully navigated to company-x base")
        return self
        
    def click_create_new(self):
        """Click the Create New button and wait for dropdown"""
        self.log_action("Clicking Create New button")
        # Wait for and click the create new button
        self.assert_element_present(*self.CREATE_NEW_BUTTON, "Create New button")
        create_new_btn = self.wait.until(EC.element_to_be_clickable(self.CREATE_NEW_BUTTON))
        assert create_new_btn.is_displayed(), "Create New button is not visible"
        create_new_btn.click()
        self.log_success("Create New button clicked")
        
        # Wait for dropdown menu to appear and verify it's visible
        self.log_action("Waiting for dropdown menu to appear")
        dropdown = self.wait.until(EC.visibility_of_element_located(self.DROPDOWN_MENU))
        assert dropdown.is_displayed(), "Dropdown menu did not appear after clicking Create New"
        self.assert_element_present(*self.DROPDOWN_MENU, "Create New dropdown menu")
        self.log_success("Dropdown menu appeared successfully")
        return self
        
    def click_table_option(self):
        """Click the Table option from the dropdown and return TablePage"""
        self.log_action("Clicking Table option from dropdown")
        # Wait for and click the table option
        self.assert_element_present(*self.TABLE_OPTION, "Table option in dropdown")
        table_option = self.wait.until(EC.element_to_be_clickable(self.TABLE_OPTION))
        assert table_option.is_displayed(), "Table option is not visible in dropdown"
        table_option.click()
        self.log_success("Table option clicked - transitioning to table creation form")
        
        # Return TablePage to handle the table creation form
        from .table_page import TablePage
        return TablePage(self.driver)
    
    def go_to_employees_table(self):
        """Navigate to company-x and then click employees table"""
        self.go_to_company_x()
        self.click_employees_table()
        return self
    
    def click_company_x_base(self):
        """Click the company-x base in the sidebar (by data-testid)"""
        self.log_action("Clicking company-x base in sidebar")
        base_btn = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-testid="nc-sidebar-base-title-company-x"]')))
        base_btn.click()
        self.log_success("Clicked company-x base")
        return self

    def click_duplicate_base(self):
        """Click the Duplicate button for company-x base using data-testid on the <li>."""
        self.log_action("Clicking Duplicate button for company-x base")
        duplicate_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "li[data-testid='nc-sidebar-base-duplicate']"))
        )
        duplicate_btn.click()
        self.log_success("Clicked Duplicate button")
        return self
  
    def click_duplicate_base_button(self):
        """Click the 'Duplicate Base' button in the modal/dialog after clicking Duplicate."""
        self.log_action("Clicking 'Duplicate Base' button in modal")
        # Try to find a button with text 'Duplicate Base' (adjust selector if needed)
        duplicate_base_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Duplicate Base') or .//*[contains(text(), 'Duplicate Base')]]"))
        )
        duplicate_base_btn.click()
        self.log_success("Clicked 'Duplicate Base' button")
        return self
    
    
    def wait_for_sidebar_load(self):
        """Wait for sidebar to load completely"""
        success = self.is_element_present(*self.SIDEBAR_BASE_BUTTON, timeout=10)
        return self if success else None
