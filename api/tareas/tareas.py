from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')