from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# Setup WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")  # Hide Selenium detection
options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Remove logging
driver = webdriver.Chrome(options=options)

# Navigate to Amazon Home
driver.get("https://www.amazon.com/")
time.sleep(random.uniform(3, 5))  # Randomized delay

# Click "Sign in" if not already signed in
try:
    sign_in_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.ID, "nav-link-accountList"))
    )
    sign_in_button.click()
    print("Clicked 'Sign in' on Amazon.")

    # Enter email
    email_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "ap_email"))
    )
    email_input.send_keys("nidarumsha@gmail.com")  # Replace with your Amazon email
    driver.find_element(By.ID, "continue").click()
    print("Entered email and clicked 'Continue'.")

    # Enter password
    password_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "ap_password"))
    )
    password_input.send_keys("crazy123")  # Replace with your Amazon password
    driver.find_element(By.ID, "signInSubmit").click()
    print("Entered password and logged in.")

    time.sleep(random.uniform(5, 7))  # Allow time for login processing

except Exception as e:
    print("Amazon login process failed or already signed in:", e)

# Get search query from user
search_query = input("Enter what you want to search for (book, author, product, etc.): ").strip()

# Perform search
try:
    search_box = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.ID, "twotabsearchtextbox"))
    )
    search_box.clear()
    search_box.send_keys(search_query)
    driver.find_element(By.ID, "nav-search-submit-button").click()
    print(f"Searched for '{search_query}' on Amazon.")

    time.sleep(random.uniform(5, 8))  # Wait for search results to load

    # Extract top 10 item names
    items = []
    
    # Try finding results with both CSS_SELECTOR and XPath as fallback
    results = WebDriverWait(driver, 15).until(
        EC.presence_of_all_elements_located(
            (By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")
        )
    )

    for result in results:
        try:
            # Extract item title
            title_element = result.find_element(By.CSS_SELECTOR, "h2 a span")
            title = title_element.text.strip()

            # Get product link
            product_link = result.find_element(By.CSS_SELECTOR, "h2 a").get_attribute("href")

            if title:
                items.append((title, product_link))

            if len(items) == 10:  # Stop after collecting 10 items
                break
        except:
            continue

    # If no results found, try fallback XPath
    if not items:
        print("Trying alternate method to fetch results...")
        results = driver.find_elements(By.XPATH, "//div[contains(@class, 's-main-slot')]//h2/a")

        for result in results:
            try:
                title = result.text.strip()
                product_link = result.get_attribute("href")

                if title:
                    items.append((title, product_link))

                if len(items) == 10:
                    break
            except:
                continue

except Exception as e:
    print("Failed to extract search results:", e)

# Display search results
if items:
    print("\nTop 10 Results Found:")
    for idx, (title, _) in enumerate(items, start=1):
        print(f"{idx}. {title}")
else:
    print("No results found. Try a different search term.")

# Ask if the user wants to add something to cart/wishlist
if items:
    choice = input("\nDo you want to add an item to cart or wishlist? (yes/no): ").strip().lower()
    if choice == "yes":
        while True:
            try:
                item_number = int(input("Enter the number of the item you want to add: "))
                if 1 <= item_number <= len(items):
                    selected_item, selected_link = items[item_number - 1]
                    break
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        # Open product page
        driver.get(selected_link)
        print(f"Opened '{selected_item}' on Amazon.")

        time.sleep(random.uniform(3, 5))  # Allow time for page to load

        # Ask what action to take
        while True:
            action = input("Do you want to (1) Buy Now, (2) Add to Cart, (3) Add to Wishlist? Enter 1/2/3: ").strip()
            if action in ["1", "2", "3"]:
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")

        try:
            if action == "1":
                buy_now_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "buy-now-button"))
                )
                buy_now_button.click()
                print("Clicked 'Buy Now'. Proceed with checkout in browser.")

            elif action == "2":
                add_to_cart_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "add-to-cart-button"))
                )
                add_to_cart_button.click()
                print(f"Added '{selected_item}' to cart.")

            elif action == "3":
                add_to_wishlist_button = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "add-to-wishlist-button-submit"))
                )
                add_to_wishlist_button.click()
                print(f"Added '{selected_item}' to wishlist.")

        except Exception as e:
            print("Action failed:", e)

# Keep browser open for debugging
input("Press Enter to close browser...")
driver.quit()
