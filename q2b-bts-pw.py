'''
Question 2: How does caching impact loading times on the Books to Scrape website, with the two navigation methods (clicking on menu vs. direct links)?
Goal B: Using Playwright, measure load times of book categories on BooksToScrape website, by directly going to links and with caching.
'''

from playwright.sync_api import sync_playwright
import time
import json

BASE_URL = "https://books.toscrape.com/"

# Categories to test with full URLs
categories = {}
with open('urls.txt', 'r') as file:
    for line in file:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        name, url = line.split(',', 1)
        categories[name] = url

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto(BASE_URL)

    for name, url in categories.items():
        start_time = time.time()
        page.goto(url)
        page.wait_for_selector("article.product_pod") 
        load_duration = (time.time() - start_time) * 1000

        # Total number of books in the category from the first <strong> tag
        total_books = int(page.locator("form.form-horizontal strong").first.inner_text())

        results.append({
            "Category": name,
            "Books Total": total_books,
            "Load Time (ms)": round(load_duration, 2)
        })

# Save to JSON
with open("q2b-bts-pw.json", "w") as f:
    json.dump(results, f, indent=2)