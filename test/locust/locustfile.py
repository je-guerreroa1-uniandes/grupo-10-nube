from locust import HttpUser, TaskSet, between, events
import logging
import random
import config


def health_check(l):
    l.client.get("/")


def login(l):
    l.client.post("/api/auth/login", data={
        "username": "username",
        "password": "password"
    })


# Para ejecutar esta prueba, se debe tener subido el archivo leviatan.png usando el cliente web
def retieve_original_file(l):
    l.client.get("/api/files/leviatan.png", headers={
        'Authorization': f'Bearer {config.G10_JWT_TOKEN}'
    })

# Para ejecutar esta prueba, se debe tener subido el archivo leviatan.png usando el cliente web
def retieve_compressed_file(l):
    l.client.get("/api/files/leviatan.zip", headers={
        'Authorization': f'Bearer {config.G10_JWT_TOKEN}'
    })


def upload_file(l):
    files = ['Image_0-270MiB.png', 'Video_2-157MiB.mp4', 'Video_4-067MiB.mp4',
             'Video_5-416MiB.mp4', 'Video_11-826MiB.mp4']
    random_number = random.randint(0, len(files))

    valid_format = ['zip', 'tar_gz', 'tar_bz2']
    random_format = random.randint(0, len(valid_format))

    with open(files[random_number], 'rb') as f:
        l.client.post("/api/tasks", data={
            "to_format": valid_format[random_format],
        }, files=[
            ("file", (files[random_number], f, "application/octet-stream"))
        ], headers={
            'Authorization': f'Bearer {config.G10_JWT_TOKEN}'
        })


@events.quitting.add_listener
def _(environment, **kw):
    if environment.stats.total.fail_ratio > 0.01:
        logging.error("Test failed due to failure ratio > 1%")
        environment.process_exit_code = 1
    elif environment.stats.total.avg_response_time > 1000:
        logging.error(
            "Test failed due to average response time ratio > 1000 ms")
        environment.process_exit_code = 2
    elif environment.stats.total.get_response_time_percentile(0.95) > 4000:
        logging.error(
            "Test failed due to 95th percentile response time > 4000 ms")
        environment.process_exit_code = 3
    else:
        environment.process_exit_code = 0


class Entrega1Escenario1(TaskSet):
    tasks = [health_check, login]


class Entrega1Escenario2(TaskSet):
    tasks = [retieve_original_file, retieve_compressed_file]


class Entrega2Escenario1(TaskSet):
    tasks = [upload_file]


class WebsiteUser(HttpUser):
    host = config.AUT_LOCATION
    wait_time = between(2, 5)
    switcher = {
        '1': Entrega1Escenario1,
        '2': Entrega1Escenario2,
        '3': Entrega2Escenario1
    }
    a_probar = switcher.get(config.G10_ESCENARIO)
    tasks = [a_probar]
