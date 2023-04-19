from locust import HttpUser, TaskSet, between


def transporte(l):
    l.client.get("/transporte")


def transporte(l):
    l.client.post("/transporte", json={
        "fecha": "2023-02-25 17:05:41"
    })


def ordencompra(l):
    l.client.get("/ordencompra")


def consultaruta(l):
    l.client.get("/consultaruta")


def ordencomprapost(l):
    l.client.post("/ordencompra", json={
        "cliente": "cliente 1",
        "evidencia_fotografica": "evidencia",
        "rutaPedido": "",
        "estadoPedido": "PAGADO",
        "puntoVenta": 1,
        "precio": "1000",
        "producto": "producto"
    })


class UserTasks(TaskSet):
    # tasks = [transporte, ordencompra, consultaruta]
    # tasks = [ordencomprapost]
    tasks = [consultaruta]


class WebsiteUser(HttpUser):
    """
    User class that does requests to the locust web server running on localhost
    """

    host = "https://api.arquitecturaccp.com"
    # wait_time = between(2, 5)
    tasks = [UserTasks]