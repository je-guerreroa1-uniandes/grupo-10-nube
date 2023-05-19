import logging
import sys
import zipfile
import zlib
import tarfile
import os
import time

from celery import Celery
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from google.cloud import pubsub_v1
from modelos import File
import config

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


celery_app = Celery(__name__)
celery_app.config_from_object(config)

subscriber = pubsub_v1.SubscriberClient()

subscription_path = subscriber.subscription_path(
    config.GOOGLE_PUBSUB_PROJECT_ID, config.GOOGLE_PUBSUB_SUBSCRIPTION_ID
)

def callback(message):
    payload = message.data.decode()
    file_id = message.attributes.get('file_id')
    filename = message.attributes.get('filename')
    new_format = message.attributes.get('new_format')
    fecha = message.attributes.get('fecha')

    print("Received message:")
    print("Payload:", payload)
    print("File ID:", file_id)
    print("Filename:", filename)
    print("New Format:", new_format)
    print("Fecha:", fecha)

    proccess_file.delay(file_id, filename, new_format, fecha)

    message.ack()

future = subscriber.subscribe(subscription_path, callback)

try:
    future.result()
except Exception as e:
    print("Error occurred:", e)


# Configure SQLAlchemy to use the PostgreSQL database
engine = create_engine(config.POSTGRES_URI)
Session = sessionmaker(bind=engine)
session = Session()


def to_zip(file_path, destination_path):
    processed_filename = destination_path + '.zip'
    with zipfile.ZipFile(processed_filename, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION) as zip_file:
        zip_file.write(file_path)
    return processed_filename


def to_tar_gz(file_path, destination_path):
    processed_filename = destination_path + '.tar.gz'
    with tarfile.open(destination_path + '.tar.gz', 'w:gz') as tar:
        print(f'file url{file_path}')
        tar.add(file_path, arcname=os.path.basename(file_path))
    return processed_filename


def to_tar_bz2(file_path, destination_path):
    processed_filename = destination_path + '.tar.bz2'
    with tarfile.open(destination_path + '.tar.bz2', 'w:bz2') as tar:
        tar.add(file_path, arcname=os.path.basename(file_path))
    return processed_filename

@celery_app.task(name='proccess_file')
def proccess_file(file_id, filename, new_format, fecha):
    UPLOAD_FOLDER = './uploads'
    PROCESS_FOLDER = './processed'
    filenameParts = filename.split('.')

    log_file_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'log_conversion.txt')
    with open(log_file_path, 'a+') as file:
        file.write(
            '{} to {} - solicitud de conversion: {}\n'.format(filename, new_format, fecha))

    formats = {
        'zip': to_zip,
        'tar_gz': to_tar_gz,
        'tar_bz2': to_tar_bz2
    }

    # Query the database for all users
    # file = session.query(File).filter_by(id=file_id).first()
    # print(f'found file:{file}')
    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    while not os.path.exists(file_path):
        logger.warning(f"File not found: {file_path}. Waiting 0.5 seconds...")
        time.sleep(0.5)
    logger.info(f"File found: {file_path}")

    if not os.path.exists(file_path):
        logger.error(f"File not found: {file_path}")
        print(f"File not found: {file_path}")
        return

    if new_format in formats.keys():
        print(f"calling {new_format}")
        func = formats[new_format]
        print(f"function: {func}")
        processed_filename = func(file_path, os.path.join(
            PROCESS_FOLDER, filenameParts[0]))
        print(f"original: {os.path.join(PROCESS_FOLDER, filename)}")
        print(f"destination: {processed_filename}")
        file = session.query(File).filter_by(id=file_id).first()
        processed_filename_parts = processed_filename.split('/')
        file.processed_filename = processed_filename_parts[-1]
        file.state = 'PROCESSED'
        session.add(file)
        session.commit()
    else:
        print("Invalid format")
