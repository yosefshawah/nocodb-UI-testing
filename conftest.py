import pytest
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage


@pytest.fixture(scope="function")
def driver():
    """Fixture to provide WebDriver instance for each test"""
    driver = DriverManager.get_chrome_driver()
    yield driver
    DriverManager.quit_driver(driver)


@pytest.fixture
def login_page(driver):
    """Fixture to provide LoginPage instance"""
    return LoginPage(driver)


@pytest.fixture
def dashboard_page(driver):
    """Fixture to provide DashboardPage instance"""
    return DashboardPage(driver)


@pytest.fixture
def logged_in_driver(driver, login_page):
    """Fixture to provide a driver that's already logged in"""
    from config.test_config import TEST_EMAIL, TEST_PASSWORD
    
    login_page.navigate_to()
    login_page.login(TEST_EMAIL, TEST_PASSWORD)
    login_page.wait_for_login_completion()
    
    yield driver
