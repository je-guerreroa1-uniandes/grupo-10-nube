import config
from celery import Celery
from google.cloud import pubsub_v1
from google.oauth2 import service_account

# Path to your service account key file
service_account_key_path = './google-json/uniandes-grupo-10-9a07a80edaf8.json'

# Load the credentials from the JSON key file
credentials = service_account.Credentials.from_service_account_file(service_account_key_path)

# Set the credentials on the Pub/Sub subscriber client
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

subscription_path = subscriber.subscription_path(
    config.GOOGLE_PUBSUB_PROJECT_ID, config.GOOGLE_PUBSUB_SUBSCRIPTION_ID
)

celery_app = Celery(__name__, broker=config.REDIS_URI)


@celery_app.task(name='process_file')
def process_file(*args):
    pass


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

    process_file.delay(file_id, filename, new_format, fecha)

    message.ack()


if __name__ == "__main__":
    future = subscriber.subscribe(subscription_path, callback)

    # Keep the script running to continue listening for messages
    try:
        future.result()
    except KeyboardInterrupt:
        future.cancel()
