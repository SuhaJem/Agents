from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def setup_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(options=options)
    return driver

def login_amazon(driver, email, password):
    driver.get("https://www.amazon.com/")
    time.sleep(3)
    
    try:
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "nav-link-accountList"))
        )
        sign_in_button.click()
        print("Clicked 'Sign in' on Amazon.")
        
        email_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_email"))
        )
        email_input.send_keys(email)
        driver.find_element(By.ID, "continue").click()
        print("Entered email and clicked 'Continue'.")
        
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ap_password"))
        )
        password_input.send_keys(password)
        driver.find_element(By.ID, "signInSubmit").click()
        print("Entered password and logged in.")
        
    except Exception as e:
        print("Amazon login process failed:", e)

def search_amazon(driver, query):
    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.clear()
    search_box.send_keys(query)
    driver.find_element(By.ID, "nav-search-submit-button").click()
    print(f"Searched for '{query}' on Amazon.")
    time.sleep(5)

def get_search_results(driver):
    books = []
    try:
        results = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.s-main-slot div.s-result-item"))
        )
        
        for result in results:
            try:
                title_element = result.find_element(By.CSS_SELECTOR, "h2 a")
                title = title_element.text.strip()
                title_element.click()
                time.sleep(3)
                
                try:
                    price_element = driver.find_element(By.CSS_SELECTOR, "span.a-price span.a-offscreen")
                    price = price_element.text.strip()
                except:
                    price = "Price not available"
                
                books.append((title, price))
                driver.back()
                time.sleep(3)
                if len(books) == 10:
                    break
            except Exception:
                continue
    except Exception as e:
        print("Failed to extract items:", e)
    return books

def add_to_cart(driver, product_name):
    try:
        search_amazon(driver, product_name)
        time.sleep(5)
        first_item = driver.find_element(By.CSS_SELECTOR, "div.s-main-slot div.s-result-item h2 a")
        first_item.click()
        time.sleep(3)
        
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "add-to-cart-button"))
        )
        add_to_cart_button.click()
        print(f"Added '{product_name}' to cart.")
        time.sleep(3)
        
    except Exception as e:
        print(f"Could not add '{product_name}' to cart:", e)

def main():
    driver = setup_driver()
    email = input("Enter your Amazon email: ")
    password = input("Enter your Amazon password: ")
    
    login_amazon(driver, email, password)
    
    query = input("Enter what you want to search for: ")
    search_amazon(driver, query)
    books = get_search_results(driver)
    
    if books:
        print("\nTop Search Results:")
        for idx, (title, price) in enumerate(books, start=1):
            print(f"{idx}. {title} - {price}")
        
        add_item = input("Do you want to add something to cart? (yes/no): ")
        if add_item.lower() == "yes":
            product_name = input("Enter the exact product name to add to cart: ")
            add_to_cart(driver, product_name)
            
    else:
        print("No results found. Try a different search term.")
    
    input("Press Enter to close browser...")
    driver.quit()

if __name__ == "__main__":
    main()
