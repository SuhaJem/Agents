from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # Hide Selenium usage
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Remove logging
driver = webdriver.Chrome(options=options)

driver.get("https://www.goodreads.com/")
time.sleep(3)  # Allow time for page to load

try:
    # Check if "Continue with Amazon" exists
    sign_in_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Continue with Amazon')]"))
    )
    print("Found the 'Continue with Amazon' button.")

    # Scroll into view
    driver.execute_script("arguments[0].scrollIntoView();", sign_in_button)
    time.sleep(1)  

    # Use ActionChains to click
    ActionChains(driver).move_to_element(sign_in_button).click().perform()
    print("Clicked using ActionChains.")
    
except Exception as e:
    print("Could not find or click the Amazon button:", e)

# Keep browser open for debugging
input("Press Enter to close browser...")
driver.quit()
