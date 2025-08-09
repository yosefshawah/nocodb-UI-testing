import pytest
from config.test_config import TEST_EMAIL, TEST_PASSWORD


def test_login_and_navigation(login_page, dashboard_page):
    """Login and navigate to test_base using POM objects."""
    login_page.navigate_to()
    login_page.login(TEST_EMAIL, TEST_PASSWORD)

    assert login_page.wait_for_login_completion(), "Login did not complete successfully"
    assert dashboard_page.is_dashboard_page(), "Not redirected to dashboard page"
    assert dashboard_page.wait_for_dashboard_load(), "Dashboard did not load properly"
    assert dashboard_page.navigate_to_test_base(), "Failed to navigate to test_base"


def test_login_page_elements(login_page):
    """Verify key login page elements exist using POM locators and helpers."""
    login_page.navigate_to()

    assert login_page.is_element_present(*login_page.EMAIL_INPUT), "Email input not found"
    assert login_page.is_element_present(*login_page.PASSWORD_INPUT), "Password input not found"
    assert login_page.is_element_present(*login_page.LOGIN_BUTTON), "Login button not found"

