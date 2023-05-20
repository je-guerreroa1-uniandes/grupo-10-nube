import config
from file_converter import FileConverter
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from celery import Celery
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos import File
import zipfile
import zlib
import tarfile
import os
import time

# Path to your service account key file
service_account_key_path = './google-json/uniandes-grupo-10-9a07a80edaf8.json'

# Load the credentials from the JSON key file
credentials = service_account.Credentials.from_service_account_file(service_account_key_path)

# Set the credentials on the Pub/Sub subscriber client
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

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

# Configure SQLAlchemy to use the PostgreSQL database
engine = create_engine(config.POSTGRES_URI)
Session = sessionmaker(bind=engine)
session = Session()

celery_app = Celery(__name__)
celery_app.config_from_object(config)

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
        'zip': FileConverter.to_zip,
        'tar_gz': FileConverter.to_tar_gz,
        'tar_bz2': FileConverter.to_tar_bz2
    }

    file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    while not os.path.exists(file_path):
        print(f"File not found: {file_path}. Waiting 0.5 seconds...")
        time.sleep(0.5)
    print(f"File found: {file_path}")

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    file_converter = FileConverter()

    if new_format == 'zip':
        processed_filename = file_converter.to_zip(file_path, os.path.join(PROCESS_FOLDER, filenameParts[0]))
    elif new_format == 'tar_gz':
        processed_filename = file_converter.to_tar_gz(file_path, os.path.join(PROCESS_FOLDER, filenameParts[0]))
    elif new_format == 'tar_bz2':
        processed_filename = file_converter.to_tar_bz2(file_path, os.path.join(PROCESS_FOLDER, filenameParts[0]))
    else:
        print("Invalid format")
        return