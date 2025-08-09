from pages.login_page import LoginPage


def test_url_navigation_uses_remote_base(login_page):
    login_page.navigate_to()
    actual_url = login_page.driver.current_url
    assert "52.18.93.49" in actual_url, f"Expected remote server in URL, got: {actual_url}"

