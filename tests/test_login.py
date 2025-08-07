import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


def test_nocodb_login():
    email = "user@gmail.com"         
    password = "EZdwS84peZttMT6"   

    url = "http://localhost:8080/dashboard/#/signin?continueAfterSignIn=/default/pa8kekibn33xfdm/mfd6v67s6a0l3tp"

    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    try:
        driver.get(url)
        time.sleep(2)  # wait for UI to load

        # Find email input by placeholder
        email_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter your work email"]')
        email_input.send_keys(email)
        time.sleep(2)  # wait for UI to load
        # Find password input by placeholder
        password_input = driver.find_element(By.XPATH, '//input[@placeholder="Enter your password"]')
        password_input.send_keys(password)
        time.sleep(2)  # wait for UI to load
        # Click the login button by data-test-id
        login_button = driver.find_element(By.CSS_SELECTOR, '[data-testid="nc-form-signin__submit"]')
        login_button.click()

        time.sleep(5)  # wait for redirect

        # Check we're no longer on sign-in
        current_url = driver.current_url
        assert "signin" not in current_url
        assert "dashboard" in current_url
        
        # ✅ Click the sidebar base button
        sidebar_base_button = driver.find_element(By.CLASS_NAME, "active-base")
        sidebar_base_button.click()
        time.sleep(2)  # Let it load or expand
        try:
            test_base_span = driver.find_element(By.XPATH, "//span[text()='test_base']")
            test_base_span.click()
            time.sleep(2)
        except Exception as e:
            print("Could not find or click 'test_base':", e)

    finally:
        driver.quit()
