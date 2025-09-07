from locust import HttpUser, task
class Buyer(HttpUser):
    @task
    def view_shop(self):
        self.client.get("/")