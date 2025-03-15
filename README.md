This project automates book searches, Amazon purchases, and general web crawling for book recommendations.

Files & Their Purpose
1. amazon.py – Logs into Amazon, searches for books, and adds them to the cart.
2. book_agent.py – Attempts to find books based on detailed tropes (Currently not fully functional).
3. book_search.py – Searches for books on different platforms (Amazon, Goodreads, etc.).
4. bookrecs.py – Compiles book recommendations from various sources.
5. books.py – General book search functionality (Some overlap with other scripts).

Run this command in your terminal
pip install -r requirements.txt

To run the amazon seacrh agent.
python amazon.py

To run the others follow same command.
python your_script.py

IMPORTANT NOTES
. This project requires Selenium and ChromeDriver.
. The Amazon bot works for Amazon India (amazon.in).

* Your password should not be stored in the code. Instead, use environment variables.

Set this variable before running the script:
export AMAZON_PASSWORD="your-password-here"  # Linux/macOS
set AMAZON_PASSWORD="your-password-here"  # Windows

The best practise is to use a virtual environment.
Here's how you can create a virtual environment, activate it, and install dependencies on both Windows and macOS/Linux.

Windows 
Open Command Prompt (cmd) or PowerShell
Navigate to your project folder:
cd path\to\your\project
python -m venv venv -> create the virtual environment
To Activate the virtual environment:
venv\Scripts\activate
You should see (venv) at the beginning of your terminal prompt.


macOS/Linux 
Open Terminal
Navigate to your project folder:
cd /path/to/your/project
Create a virtual environment:
python3 -m venv venv
Activate the virtual environment:
source venv/bin/activate

Install dependencies using 
pip install -r requirements.txt

use 'deactivate' to deactivate virtual environment

Why these requirements?
selenium ->	Automates web browsing for Amazon search and cart handling
beautifulsoup4 ->	Parses and extracts book information from web pages
requests ->	Sends HTTP requests to fetch book data
lxml ->	Faster and more efficient HTML parsing for scraping
undetected-chromedriver	-> Helps avoid bot detection on Amazon
tqdm ->	Displays progress bars for web crawling
