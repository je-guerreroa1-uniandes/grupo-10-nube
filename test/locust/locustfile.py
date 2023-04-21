from locust import HttpUser, TaskSet, between


def health_check(l):
    l.client.get("/api")


def login(l):
    l.client.post("/api/auth/login", json={
        "username": "usuario",
        "password": "contrasenia"
    })


class Escenario1(TaskSet):
    tasks = [health_check, login]


class WebsiteUser(HttpUser):
    """
    User class that does requests to the locust web server running on the cloud
    """

    host = "http://grupo10nube.com"
    wait_time = between(2, 5)
    tasks = [Escenario1]
