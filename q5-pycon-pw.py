# Question 5: How do different years of PyCon websites perform in terms of load time?
# Goal: Measure the load time of PyCon websites from 2016 to 2025 using Playwright.

import asyncio
from playwright.async_api import async_playwright
import time

urls = [f"https://{year}.pycon.co" for year in range(2016, 2026)]

async def run():
    results = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        for url in urls:
            context = await browser.new_context()  # Cold start
            page = await context.new_page()
            try:
                start = time.time()
                response = await page.goto(url, wait_until="load", timeout=15000)
                load_time = time.time() - start
                if response and response.ok:
                    print(f"{url} -> {load_time:.2f}s")
                    results[url] = load_time
                else:
                    print(f"{url} -> failed with status: {response.status if response else 'No Response'}")
                    results[url] = None
            except Exception as e:
                print(f"{url} -> error: {str(e)}")
                results[url] = None
            await context.close()
        await browser.close()
    return results

asyncio.run(run())