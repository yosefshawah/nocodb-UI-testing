from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


class DriverManager:
    """Utility class to manage WebDriver setup and configuration"""
    
    @staticmethod
    def get_chrome_driver():
        """Get configured Chrome WebDriver instance"""
        chrome_options = Options()
        
        # Performance optimizations
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Optional: Add headless mode for CI/CD
        # chrome_options.add_argument("--headless")
        
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
