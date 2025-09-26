import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """Utility class to manage WebDriver setup and configuration"""
    
    @staticmethod
    def _is_ci_environment():
        """Detect if running in CI environment"""
        ci_indicators = [
            'CI',           # Generic CI indicator
            'GITHUB_ACTIONS',  # GitHub Actions
            'GITLAB_CI',    # GitLab CI
            'JENKINS_URL',  # Jenkins
            'TRAVIS',       # Travis CI
            'CIRCLECI',     # CircleCI
            'BUILDKITE',    # Buildkite
            'DRONE',        # Drone CI
            'TEAMCITY_VERSION',  # TeamCity
        ]
        return any(os.getenv(var) for var in ci_indicators)
    
    @staticmethod
    def _should_run_headless():
        """Determine if browser should run in headless mode"""
        # Check explicit environment variable first
        headless_env = os.getenv('HEADLESS', '').lower()
        if headless_env in ('1', 'true', 'yes', 'on'):
            return True
        elif headless_env in ('0', 'false', 'no', 'off'):
            return False
        
        # Default to headless in CI environments
        return DriverManager._is_ci_environment()
    
    @staticmethod
    def get_chrome_driver(enable_performance_logging=False):
        """Get configured Chrome WebDriver instance
        
        Args:
            enable_performance_logging (bool): Enable performance/network logging
        """
        chrome_options = Options()
        
        # Always use incognito mode for clean browser storage
        chrome_options.add_argument("--incognito")
        
        # Performance optimizations
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Enable performance logging if requested
        if enable_performance_logging:
            chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        
        # Headless mode detection with debugging
        is_headless = DriverManager._should_run_headless()
        is_ci = DriverManager._is_ci_environment()
        headless_env = os.getenv('HEADLESS', '')
        
        print(f"[debug] CI environment detected: {is_ci}")
        print(f"[debug] HEADLESS env var: '{headless_env}'")
        print(f"[debug] Should run headless: {is_headless}")
        
        if is_headless:
            chrome_options.add_argument("--headless")
            print("🤖 Running in headless mode")
        else:
            print("🖥️ Running in windowed mode")
        
        # Additional CI-specific optimizations
        if DriverManager._is_ci_environment():
            chrome_options.add_argument("--disable-background-timer-throttling")
            chrome_options.add_argument("--disable-backgrounding-occluded-windows")
            chrome_options.add_argument("--disable-renderer-backgrounding")
            chrome_options.add_argument("--disable-features=TranslateUI")
            chrome_options.add_argument("--disable-ipc-flooding-protection")
            
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Set shorter implicit wait for faster execution
        driver.implicitly_wait(3)
        
        # Set page load timeout
        driver.set_page_load_timeout(10)
        
        return driver
    
    @staticmethod
    def quit_driver(driver):
        """Safely quit the WebDriver"""
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error quitting driver: {e}")
