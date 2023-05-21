import os
import time
import config
from google.cloud import pubsub_v1
from google.oauth2 import service_account
from google.cloud import storage
from werkzeug.utils import secure_filename
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

from file_converter import FileConverter
from modelos import File

# Configure SQLAlchemy to use the PostgreSQL database
engine = create_engine(config.POSTGRES_URI)
Session = sessionmaker(bind=engine)
session = Session()

# Path to your service account key file
service_account_key_path = './google-json/uniandes-grupo-10-9a07a80edaf8.json'

# Load the credentials from the JSON key file
credentials = service_account.Credentials.from_service_account_file(service_account_key_path)

# Set the credentials on the Pub/Sub subscriber client
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

subscription_path = subscriber.subscription_path(
    config.GOOGLE_PUBSUB_PROJECT_ID, config.GOOGLE_PUBSUB_SUBSCRIPTION_ID
)

# Create a client instance with the specified service account key
client = storage.Client.from_service_account_json(service_account_key_path)

# Specify the bucket name
bucket_name = config.G10_CLOUD_BUCKET

bucket = client.get_bucket(bucket_name)

# List the blobs in the bucket
blobs = bucket.list_blobs()
for blob in blobs:
    print(blob.name)


def callback(message):
    payload = message.data.decode()
    file_id = message.attributes.get('file_id')
    filename = message.attributes.get('filename')
    new_format = message.attributes.get('new_format')

    print("Received message:")
    print("Payload:", payload)
    print("File ID:", file_id)
    print("Filename:", filename)
    print("New Format:", new_format)

    process_file(file_id, filename, new_format)

    message.ack()


def process_file(file_id, filename, new_format):
    UPLOAD_FOLDER = '/tmp/uploads'
    PROCESS_FOLDER = '/tmp/processed'
    filename_parts = filename.split('.')

    file = session.query(File).filter_by(id=file_id).first()
    log_file_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'log_conversion.txt')
    with open(log_file_path, 'a+') as log_file:
        log_file.write(
            '{} to {} - solicitud de conversion: {}\n'.format(filename, new_format, file.created_at)) #datetime.utcnow()))

    formats = {
        'zip': FileConverter.to_zip,
        'tar_gz': FileConverter.to_tar_gz,
        'tar_bz2': FileConverter.to_tar_bz2
    }

    file_path = secure_filename(filename)
    blob = bucket.blob(file_path)

    if not blob.exists():
        print(f"Blob not found: {file_path}")
        return

    # Download the file to the local temporary directory
    temp_file_path = os.path.join(UPLOAD_FOLDER, secure_filename(filename))
    blob.download_to_filename(temp_file_path)

    if new_format in formats.keys():
        print(f"Calling {new_format}")
        func = formats[new_format]
        print(f"Function: {func}")

        # Convert the file
        processed_filename = func(temp_file_path, os.path.join(
            PROCESS_FOLDER, filename_parts[0]))

        # Upload the processed file to Cloud Storage
        processed_blob = bucket.blob(processed_filename)
        processed_blob.upload_from_filename(processed_filename)

        print(f"Original: {file_path}")
        print(f"Destination: {processed_filename}")

        processed_filename_parts = processed_filename.split('/')
        file.processed_filename = processed_filename_parts[-1]
        file.state = 'PROCESSED'

        # Delete the temporary files
        os.remove(temp_file_path)
        os.remove(processed_filename)

        session.add(file)
        session.commit()
    else:
        print("Invalid format")

if __name__ == "__main__":
    future = subscriber.subscribe(subscription_path, callback)

    # Keep the script running to continue listening for messages
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()
