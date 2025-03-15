import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    """Sets up a Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def search_goodreads(query):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.goodreads.com/")

    try:
        # Wait up to 15 seconds for the search bar to appear (increase timeout)
        wait = WebDriverWait(driver, 15)
        search_box = wait.until(
    EC.presence_of_element_located((By.XPATH, "//input[contains(@class, 'searchBox__input--navbar')]"))
)


        # Type search query and press Enter
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        print("Search successful!")
    except Exception as e:
        print("Error:", e)
    finally:
        driver.quit()


def search_reddit(query):
    """Searches Reddit for book recommendations in discussions."""
    driver = setup_driver()
    search_url = f"https://www.reddit.com/search/?q={query.replace(' ', '%20')}+book+recommendation"
    driver.get(search_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    posts = soup.select("a[href*='/r/books/comments']")[:5]  # Get top 5 discussion links

    results = []
    for post in posts:
        title = post.get_text(strip=True)
        link = "https://www.reddit.com" + post["href"]
        results.append({"title": title, "link": link, "source": "Reddit"})

    driver.quit()
    return results

def search_kindle(query):
    """Searches Amazon Kindle for books based on a query."""
    driver = setup_driver()
    search_url = f"https://www.amazon.com/s?k={query.replace(' ', '+')}&i=digital-text"
    driver.get(search_url)
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    books = soup.select("h2 a")[:5]  # Get top 5 book links

    results = []
    for book in books:
        title = book.get_text(strip=True)
        link = "https://www.amazon.com" + book["href"]
        results.append({"title": title, "link": link, "source": "Kindle (Amazon)"})

    driver.quit()
    return results

def get_book_recommendations(query):
    """Fetches book recommendations from Goodreads, Reddit, and Kindle."""
    print("\nSearching for book recommendations...\n")
    results = []
    results.extend(search_goodreads(query))
    results.extend(search_reddit(query))
    results.extend(search_kindle(query))
    
    return results

# Get user input dynamically
user_query = input("Enter your book preference (e.g., genre, trope, author): ").strip()

# Fetch and display results
recommendations = get_book_recommendations(user_query)

print("\nTop Book Recommendations:\n")
for book in recommendations:
    print(f"[{book['source']}] {book['title']} - {book['link']}")
