from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_open_localhost():
    options = Options()
    options.binary_location = "/snap/bin/chromium"  # Use your snap chromium binary here
    options.add_argument("--headless")  # Run without UI
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())  # downloads compatible chromedriver automatically
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("http://192.168.144.1:8080")
    print("Page title is:", driver.title)

    driver.quit()

if __name__ == "__main__":
    test_open_localhost()
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

def test_localhost_title():
    options = Options()
    # Remove the next line if you want to see the browser window
  

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.get("http://localhost:8080")
    
    print("Page Title:", driver.title)
    driver.quit()

if __name__ == "__main__":
    test_localhost_title()
