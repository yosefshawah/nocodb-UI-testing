import pytest
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.sidebar_page import SidebarPage
import subprocess
import time
import os
import requests
from config.config import BASE_URL


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
def sidebar_page(driver):
    """Fixture to provide SidebarPage instance"""
    return SidebarPage(driver)


@pytest.fixture
def logged_in_driver(driver, login_page):
    """Fixture to provide a driver that's already logged in"""
    from config.config import TEST_EMAIL, TEST_PASSWORD
    
    login_page.navigate_to()
    login_page.login(TEST_EMAIL, TEST_PASSWORD)
    login_page.wait_for_login_completion()
    
    yield driver


# --- Remote DB reset + health-check fixtures ---
SSH_HOST = os.environ.get("SSH_HOST", "ec2-52-18-93-49.eu-west-1.compute.amazonaws.com")
SSH_USER = os.environ.get("SSH_USER", "ubuntu")
SSH_KEY_FILE = os.environ.get("SSH_KEY_FILE", "/Users/shawahyosef/Desktop/nocodb-final-project/nocodb-final-yosef.pem")
RESET_SCRIPT = os.environ.get("RESET_SCRIPT", "/home/ubuntu/app/scripts/reset_db.sh")


def _wait_healthy(url: str, timeout: int = 40):
    t0 = time.time()
    if not url.endswith('/'):
        url = url + '/'
    while time.time() - t0 < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code in (200, 302):
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise TimeoutError("Service not healthy")


def _should_reset_remote_db() -> bool:
    """Decide whether to run remote DB reset based on environment.

    Set NC_REMOTE_RESET to one of: '1'/'true' to enable, '0'/'false' to disable.
    Default is '1' (enabled), but if BASE_URL looks local, default to disabled.
    """
    env_val = os.getenv("NC_REMOTE_RESET")
    if env_val is not None:
        return env_val.lower() in ("1", "true", "yes", "y", "on")

    # If BASE_URL points to localhost, default to not resetting remotely
    lowered = (BASE_URL or "").lower()
    if any(k in lowered for k in ("localhost", "127.0.0.1", "0.0.0.0")):
        return False
    return True


def reset_remote_db():
    subprocess.run([
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-i", SSH_KEY_FILE,
        f"{SSH_USER}@{SSH_HOST}",
        f"bash {RESET_SCRIPT}"
    ], check=True)


@pytest.fixture(scope="session", autouse=True)
def service_up():
    t0 = time.time()
    _wait_healthy(BASE_URL)
    print(f"[timing] Service health check: {time.time() - t0:.2f}s")
    yield


@pytest.fixture(autouse=True)
def reset_db_before_each_test(service_up, request: pytest.FixtureRequest):
    if _should_reset_remote_db():
        t_reset = time.time()
        reset_remote_db()
        _wait_healthy(BASE_URL)
        print(f"[timing] {request.node.nodeid} reset+health: {time.time() - t_reset:.2f}s")

    t_test = time.time()
    yield
    print(f"[timing] {request.node.nodeid} test duration: {time.time() - t_test:.2f}s")
