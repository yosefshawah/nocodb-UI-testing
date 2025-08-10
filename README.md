# NocoDB UI Testing Framework

A comprehensive UI testing framework for NocoDB using Selenium WebDriver, pytest, and the Page Object Model (POM) pattern with fluent interface support.

## Features

1. **Page Object Model**: Organized page objects for maintainable tests
2. **Fluent Interface**: Method chaining for readable test flows
3. **Explicit Waits**: Built-in explicit waits for better reliability
4. **Universal Components**: Reusable page objects for common functionality
5. **Method Chaining**: Fluent interface for complex user journeys

## Key Components

### BasePage (`pages/base_page.py`)

- Common functionality for all page objects
- Explicit wait methods
- Element interaction methods
- URL and navigation utilities

### LoginPage (`pages/login_page.py`)

- Login-specific functionality with method chaining
- `login_as_valid_user()` returns SidebarPage for chaining
- Email and password input methods
- Login completion verification

### SidebarPage (`pages/sidebar_page.py`)

- Universal sidebar functionality
- `go_to_company_x()` returns EmployeePage for chaining
- Navigation to different bases
- Sidebar load verification

### EmployeePage (`pages/employee_page.py`)

- Employee management functionality
- `add_employee_and_get_confirmation()` returns confirmation message
- Form filling and validation
- Success message handling

### DriverManager (`utils/driver_manager.py`)

- WebDriver setup and configuration
- Chrome options management
- Safe driver cleanup

### TestConfig (`config/test_config.py`)

- Centralized test data
- URLs and credentials
- Timeout configurations

## Running Tests

### Run the user journey test:

```bash
pytest tests/test_user_journey.py -v
```

### Run all tests:

```bash
pytest tests/ -v
```

### Run with detailed output:

```bash
pytest tests/ -v -s
```

## Example Test Flow

```python
def test_user_journey_through_employee_management(driver):
    login_page = LoginPage(driver)

    employee_confirmation_message = (
        login_page
        .login_as_valid_user()
        .go_to_company_x()
        .add_employee_and_get_confirmation(
            first_name="John",
            last_name="Doe",
            email="john.doe@company.com",
            hire_date="2024-01-15",
            salary=70000,
            role_id=2,  # Developer
            department_id=1  # IT
        )
    )

    assert "Employee added successfully" in employee_confirmation_message
```

## Adding New Tests

1. **Create new page objects** in the `pages/` directory
2. **Extend BasePage** for common functionality
3. **Add locators** as class variables
4. **Create methods** that return the next page object for chaining
5. **Write tests** using the fluent interface pattern

## Example: Adding a New Page

```python
# pages/new_page.py
from selenium.webdriver.common.by import By
from .base_page import BasePage

class NewPage(BasePage):
    # Locators
    ELEMENT_LOCATOR = (By.ID, "element-id")

    def perform_action(self):
        self.click_element(*self.ELEMENT_LOCATOR)
        return self  # For chaining

    def perform_action_and_get_result(self):
        self.perform_action()
        return self.get_result()  # Return data for assertions
```

## Best Practices

1. **Use method chaining** for fluent interfaces
2. **Return next page objects** from navigation methods
3. **Return data** from final methods for assertions
4. **Keep locators in page objects** not in tests
5. **Use meaningful method names** that describe the action
6. **Handle exceptions gracefully** in page objects
7. **Use configuration files** for test data
8. **Write descriptive test names** and assertions

## Dependencies

- `selenium`: WebDriver automation
- `pytest`: Testing framework
- `webdriver-manager`: Automatic WebDriver management
