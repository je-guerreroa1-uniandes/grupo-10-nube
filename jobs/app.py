# import time
#
# while True:
#     print('Jobs component is running...')
#     time.sleep(1)

import os
from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

@celery_app.task(name='proccess_file')
def proccess_file(filename, new_format, fecha):
    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_conversion.txt')
    with open(log_file_path, 'a+') as file:
        file.write('{} to {} - solicitud de conversion: {}\n'.format(filename, new_format, fecha))