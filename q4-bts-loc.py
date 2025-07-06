# To run: locust -f q4-bts-loc.py --host https://books.toscrape.com -u 25 -r 5 --run-time 30s

from locust import HttpUser, task, between

class BooksHomepageUser(HttpUser):
    wait_time = between(1, 3)

    @task
    def load_homepage(self):
        self.client.get("/")