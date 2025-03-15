import requests
from bs4 import BeautifulSoup
import re

def search_goodreads(trope):
    search_url = f"https://www.goodreads.com/search?q={trope.replace(' ', '+')}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch Goodreads results.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    book_links = []
    
    for link in soup.select("a.bookTitle"):
        book_links.append("https://www.goodreads.com" + link.get('href'))
        if len(book_links) >= 5:  # Get top 5 results
            break
    
    return book_links

def search_reddit(trope):
    search_url = f"https://www.reddit.com/r/RomanceBooks/search/?q={trope.replace(' ', '+')}&restrict_sr=1"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch Reddit results.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    post_links = []
    
    for link in soup.find_all("a", href=True):
        if re.search(r"/r/RomanceBooks/comments/", link['href']):
            post_links.append("https://www.reddit.com" + link['href'])
            if len(post_links) >= 5:
                break
    
    return post_links

def search_amazon(trope):
    search_url = f"https://www.amazon.com/s?k={trope.replace(' ', '+')}+book"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(search_url, headers=headers)
    
    if response.status_code != 200:
        print("Failed to fetch Amazon results.")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    book_links = []
    
    for link in soup.select("h2 a.a-link-normal"):
        book_links.append("https://www.amazon.com" + link.get('href'))
        if len(book_links) >= 5:
            break
    
    return book_links

if __name__ == "__main__":
    trope = input("Enter the book trope you are looking for: ")
    print("Searching for books...")
    
    goodreads_links = search_goodreads(trope)
    reddit_links = search_reddit(trope)
    amazon_links = search_amazon(trope)
    
    print("\nGoodreads Recommendations:")
    for link in goodreads_links:
        print(link)
    
    print("\nReddit Discussions:")
    for link in reddit_links:
        print(link)
    
    print("\nAmazon Listings:")
    for link in amazon_links:
        print(link)

