from locust import HttpUser, task, between
import threading

class WebsiteUser(HttpUser):
    wait_time = between(1, 2)
    
    # Thread-safe counter for assigning user numbers
    user_counter = 0
    user_counter_lock = threading.Lock()

    def on_start(self):
        with WebsiteUser.user_counter_lock:
            WebsiteUser.user_counter += 1
            self.user_id = WebsiteUser.user_counter

        self.email = f"user{self.user_id}@example.com"
        self.password = "test123"

        self.client.post("/register", json={
            "email": self.email,
            "password": self.password,
            "confirm": self.password
        })

        self.client.post("/login", json={
            "email": self.email,
            "password": self.password
        })

    @task
    def view_home(self):
        self.client.get("/home")

    @task
    def add_info(self):
        self.client.post("/add-info", json={
            "fname": "John",
            "mname": "A.",
            "lname": "Doe",
            "age": 25,
            "address": "123 Street",
            "bday": "2000-01-01"
        })
        print(f"User {self.user_id}: Done Queue")
