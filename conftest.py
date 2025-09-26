import pytest
from utils.driver_manager import DriverManager
from pages.login_page import LoginPage
from pages.sidebar_page import SidebarPage
import subprocess
import time
import os
import requests
import sys
from pathlib import Path
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
SSH_KEY_FILE =  os.environ.get("KEY_FILE")or os.environ.get("EC2_SSH_KEY")  or "/Users/shawahyosef/Desktop/nocodb-final-project/nocodb-final-yosef.pem"
RESET_SCRIPT = os.environ.get("RESET_SCRIPT", "/home/ubuntu/app/scripts/reset_db.sh")


def _wait_healthy(url: str, timeout: int = 40):
    if not url:
        raise ValueError("URL cannot be None or empty")
    
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
    # Debug SSH configuration
    print(f"[debug] SSH_HOST: {SSH_HOST}")
    print(f"[debug] SSH_USER: {SSH_USER}")
    print(f"[debug] SSH_KEY_FILE: {SSH_KEY_FILE}")
    print(f"[debug] RESET_SCRIPT: {RESET_SCRIPT}")
    
    # Validate SSH key file exists
    if not SSH_KEY_FILE or not os.path.exists(SSH_KEY_FILE):
        raise FileNotFoundError(f"SSH key file not found: {SSH_KEY_FILE}")
    
    # Check key file permissions
    import stat
    key_stat = os.stat(SSH_KEY_FILE)
    key_perms = stat.filemode(key_stat.st_mode)
    print(f"[debug] SSH key permissions: {key_perms}")
    
    subprocess.run([
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-i", SSH_KEY_FILE,
        f"{SSH_USER}@{SSH_HOST}",
        f"bash {RESET_SCRIPT}"
    ], check=True)


def _should_reset_local_db() -> bool:
    """Decide whether to run local DB reset based on environment.
    
    Returns True if BASE_URL points to localhost/127.0.0.1, False otherwise.
    """
    lowered = (BASE_URL or "").lower()
    return any(k in lowered for k in ("localhost", "127.0.0.1", "0.0.0.0"))


def reset_local_db():
    """Stop the NocoDB container, reset the local database, then start the container again before each test."""
    import os
    print("[debug] Stopping NocoDB container...")
    os.system("docker compose stop noco")
    script_path = os.path.join(os.path.dirname(__file__), 'scripts', 'reset_local_db.sh')
    print(f"[debug] Running local reset script: {script_path}")
    exit_code = os.system(script_path)
    print(f"[debug] Local database reset script finished with exit code {exit_code}")
    if exit_code != 0:
        raise RuntimeError(f"reset_local_db.sh failed with exit code {exit_code}")
    print("[debug] Starting NocoDB container...")
    os.system("docker compose start noco")


@pytest.fixture(scope="session", autouse=True)
def service_up():
    # Debug information for CI
    print(f"[debug] BASE_URL from config: {BASE_URL}")
    print(f"[debug] Environment BASE_URL: {os.getenv('BASE_URL')}")
    print(f"[debug] Environment NOCODB_URL: {os.getenv('NOCODB_URL')}")
    print(f"[debug] Environment EC2_HOST: {os.getenv('EC2_HOST')}")
    print(f"[debug] Environment KEY_FILE: {os.getenv('KEY_FILE')}")
    print(f"[debug] Environment SSH_KEY_FILE: {os.getenv('SSH_KEY_FILE')}")
    print(f"[debug] Final SSH_KEY_FILE: {SSH_KEY_FILE}")
    
    t0 = time.time()
    _wait_healthy(BASE_URL)
    print(f"[timing] Service health check: {time.time() - t0:.2f}s")
    yield


@pytest.fixture(autouse=True)
def reset_db_before_each_test(service_up, request: pytest.FixtureRequest):
    t_reset = time.time()
    
    if _should_reset_local_db():
        # Reset local database when running against localhost
        print(f"[debug] Running local database reset for {request.node.nodeid}")
        reset_local_db()
        _wait_healthy(BASE_URL)
        print(f"[timing] {request.node.nodeid} local reset+health: {time.time() - t_reset:.2f}s")
    elif _should_reset_remote_db():
        # Reset remote database when running against remote server
        print(f"[debug] Running remote database reset for {request.node.nodeid}")
        reset_remote_db()
        _wait_healthy(BASE_URL)
        print(f"[timing] {request.node.nodeid} remote reset+health: {time.time() - t_reset:.2f}s")
    else:
        print(f"[debug] No database reset configured for {request.node.nodeid}")

    t_test = time.time()
    yield
    print(f"[timing] {request.node.nodeid} test duration: {time.time() - t_test:.2f}s")
