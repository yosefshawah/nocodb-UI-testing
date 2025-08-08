# NocoDB Testing UI - Page Object Model

This project has been refactored to use the Page Object Model (POM) pattern for better maintainability, reusability, and test organization.

## Project Structure

```
nocodb-testing-UI/
├── pages/                    # Page Object classes
│   ├── __init__.py
│   ├── base_page.py         # Base page with common functionality
│   ├── login_page.py        # Login page object
│   └── dashboard_page.py    # Dashboard page object
├── utils/                    # Utility classes
│   ├── __init__.py
│   └── driver_manager.py    # WebDriver management
├── config/                   # Configuration files
│   ├── __init__.py
│   └── test_config.py       # Test data and settings
├── tests/                    # Test files
│   ├── test_login.py        # Original test (legacy)
│   └── test_login_pom.py    # New POM-based test
├── requirements.txt
└── README.md
```

## Page Object Model Benefits

1. **Separation of Concerns**: UI elements and test logic are separated
2. **Reusability**: Page objects can be reused across multiple tests
3. **Maintainability**: Changes to UI elements only require updates in page objects
4. **Readability**: Tests are more readable and business-focused
5. **Explicit Waits**: Built-in explicit waits for better reliability

## Key Components

### BasePage (`pages/base_page.py`)

- Common functionality for all page objects
- Explicit wait methods
- Element interaction methods
- URL and navigation utilities

### LoginPage (`pages/login_page.py`)

- Login-specific functionality
- Email and password input methods
- Login button interaction
- Login completion verification

### DashboardPage (`pages/dashboard_page.py`)

- Dashboard-specific functionality
- Sidebar navigation
- Test base navigation
- Dashboard verification methods

### DriverManager (`utils/driver_manager.py`)

- WebDriver setup and configuration
- Chrome options management
- Safe driver cleanup

### TestConfig (`config/test_config.py`)

- Centralized test data
- URLs and credentials
- Timeout configurations

## Running Tests

### Run the new POM-based test:

```bash
pytest tests/test_login_pom.py -v
```

### Run all tests:

```bash
pytest tests/ -v
```

### Run with detailed output:

```bash
pytest tests/ -v -s
```

## Adding New Tests

1. **Create new page objects** in the `pages/` directory
2. **Extend BasePage** for common functionality
3. **Add locators** as class variables
4. **Create methods** for page-specific actions
5. **Write tests** that use the page objects

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
```

## Best Practices

1. **Use explicit waits** instead of `time.sleep()`
2. **Keep locators in page objects** not in tests
3. **Use meaningful method names** that describe the action
4. **Handle exceptions gracefully** in page objects
5. **Use configuration files** for test data
6. **Write descriptive test names** and assertions

## Migration from Original Test

The original test in `tests/test_login.py` has been preserved for reference. The new POM-based test in `tests/test_login_pom.py` provides the same functionality with better structure and maintainability.

## Dependencies

- `selenium`: WebDriver automation
- `pytest`: Testing framework
- `webdriver-manager`: Automatic WebDriver management
