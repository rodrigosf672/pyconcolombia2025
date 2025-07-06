'''
Question 2: How does caching impact loading times on the Books to Scrape website, with the two navigation methods (clicking on menu vs. direct links)?
Goal A: Using Playwright, measure load times of book categories on BooksToScrape website, by clicking on categories and with caching.
'''

from playwright.sync_api import sync_playwright
import time
import json

# This script uses Playwright to measure the load time of category pages on the Books to Scrape website.
BASE_URL = "https://books.toscrape.com/"

# List of categories to test (visible text on the page's left sidebar)
categories = [
    "Travel", "Mystery", "Historical Fiction", "Sequential Art", "Classics",
    "Philosophy", "Romance", "Womens Fiction", "Fiction", "Childrens",
    "Religion", "Nonfiction", "Music", "Default", "Science Fiction", "Sports and Games",
    "Fantasy", "New Adult", "Young Adult", "Science", "Poetry", "Paranormal",
    "Art", "Psychology", "Autobiography", "Parenting", "Adult Fiction",
    "Humor", "Horror", "History", "Food and Drink", "Christian Fiction",
    "Business", "Biography", "Thriller", "Contemporary", "Spirituality",
    "Academic", "Self Help", "Historical", "Christian", "Suspense",
    "Short Stories", "Novels", "Health", "Politics", "Cultural", "Erotica",
    "Crime"
]

results = []

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    for category_name in categories:

        # Step 1: Go to home
        page.goto(BASE_URL)
        page.wait_for_selector("ul.nav-list")

        # Step 2: Click category and measure load time from Home → Category
        with page.expect_navigation():
            page.get_by_text(category_name, exact=True).click()

        page.wait_for_selector("article.product_pod")

        # Step 3: Get number of books
        total_books = int(page.locator("form.form-horizontal strong").first.inner_text())

        # Step 4: Reload and measure time
        start_time = time.time()
        page.reload()
        page.wait_for_selector("article.product_pod")
        load_duration = (time.time() - start_time) * 1000  # ms

        results.append({
            "Category": category_name,
            "Books Total": total_books,
            "Load Time (ms)": round(load_duration, 2)
        })

    # Step 5: Clean up
    browser.close()

# Save to JSON
with open("q2a-bts-pw.json", "w") as f:
    json.dump(results, f, indent=2)
