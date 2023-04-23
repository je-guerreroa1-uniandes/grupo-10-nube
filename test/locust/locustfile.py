from locust import HttpUser, TaskSet, between

TOKEN: str = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY4MjA4MTc3NSwianRpIjoiMTQwOTkxZDYtN2Y1ZS00ZjBhLWE4NjUtODU2MzY4MDdmMTJjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6eyJ1c2VybmFtZSI6InVzZXJuYW1lIiwiZW1haWwiOiJlbWFpbCIsImlkIjoxfSwibmJmIjoxNjgyMDgxNzc1LCJleHAiOjE2ODIwODI2NzV9.52_9HZ92hNdM_oxvr4j5Kohy1dncZ6rjRBMhLci5fRc"


def health_check(l):
    l.client.get("/api")


def login(l):
    l.client.post("/api/auth/login", data={
        "username": "username",
        "password": "password"
    })


def retieve_original_file(l):
    l.client.get("/api/files/leviatan.png", headers={
        'Authorization': f'Bearer {TOKEN}'
    })

def retieve_compressed_file(l):
    l.client.get("/api/files/leviatan.zip", headers={
        'Authorization': f'Bearer {TOKEN}'
    })


class Escenario1(TaskSet):
    tasks = [health_check, login]


class Escenario2(TaskSet):
    tasks = [retieve_original_file, retieve_compressed_file]


class WebsiteUser(HttpUser):
    # host = "http://grupo10nube.com"
    host = "http://localhost:8888"
    wait_time = between(2, 5)
    tasks = [Escenario2]
