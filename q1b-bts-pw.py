'''
Question 2: How does the method of navigation (clicking on menu vs. direct links) impact loading times on the Books to Scrape website?
Goal B: Using Playwright, measure load times of book categories on BooksToScrape website, by directly going to links and with NO caching.
'''

from playwright.sync_api import sync_playwright
import time
import json

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
    for name, url in categories.items():
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        start_time = time.time()
        page.goto(url)
        page.wait_for_selector("article.product_pod") 
        load_duration = (time.time() - start_time) * 1000 #ms

        # Total number of books in the category from the first <strong> tag
        total_books = int(page.locator("form.form-horizontal strong").first.inner_text())

        results.append({
            "Category": name,
            "Books Total": total_books,
            "Load Time (ms)": round(load_duration, 2)
        })

        browser.close()

with open("q1b-bts-pw.json", "w") as f:
    json.dump(results, f, indent=2)
