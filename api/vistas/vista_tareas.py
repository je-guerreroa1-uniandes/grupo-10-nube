import json
import os
import time

from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import secure_filename
# Celery for message broking
from datetime import datetime
from modelos import db, Usuario, UsuarioSchema, File, FileSchema
from google.cloud import storage
from google.oauth2 import service_account
from google.cloud import pubsub_v1
from google.cloud.pubsub_v1.publisher.futures import Future
import config

file_schema = FileSchema()

# Create credentials using the service account key
credentials = service_account.Credentials.from_service_account_file(
    config.G10_SERVICE_ACCOUNT_KEY_PATH,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Create a client instance with the specified service account key
client = storage.Client.from_service_account_json(
    config.G10_SERVICE_ACCOUNT_KEY_PATH)

bucket_name = config.G10_CLOUD_BUCKET
bucket = client.get_bucket(bucket_name)

# Initialize Google Pub/Sub publisher client with the credentials
publisher = pubsub_v1.PublisherClient(credentials=credentials)


def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'mp4'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class VistaCreateTasks(Resource):

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()  # Retrieve the ID of the current user
        print(f'current user {current_user}')

        files = File.query.filter(
            File.user_id == current_user['id']
        ).all()
        return [file_schema.dump(file) for file in files]

        # return {'mensaje': 'tarea creada exitosamente', 'usuario': current_user}

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        destination_format = request.form.get("to_format")
        print(f'to format -> {destination_format}')

        # Check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filenameParts = file.filename.split('.')
            new_filename = f"{filenameParts[0]}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.{filenameParts[-1]}"
            blob_name = f"general/uploads/{new_filename}"
            blob = bucket.blob(blob_name)
            blob.upload_from_file(file)

        new_file = File(
            filename=secure_filename(new_filename),
            to_extension=destination_format,
            processed_filename='',
            state='UPLOADED',
            user_id=current_user['id'],
            created_at=datetime.utcnow()
        )
        db.session.add(new_file)
        db.session.commit()

        response_string = {
            'mensaje': 'tarea creada exitosamente',
            'file': file_schema.dump(new_file)
        }

        # Call the message broker for queuing the file
        message = {
            'file_id': new_file.id,
            'filename': new_filename,
            'destination_format': destination_format
        }
        message_data = json.dumps(message).encode('utf-8')

        message_id = self.publish_message(
            message_data, new_file.id, new_filename, destination_format)
        print(f'Published message with ID: {message_id}')

        return response_string, 200

    def publish_message(self, payload, file_id, filename, new_format) -> Future:
        topic_path = publisher.topic_path(
            config.GOOGLE_PUBSUB_PROJECT_ID, config.GOOGLE_PUBSUB_TOPIC_NAME)

        message = pubsub_v1.types.PubsubMessage(
            data=payload,
            attributes={
                'file_id': str(file_id),
                'filename': str(filename),
                'new_format': str(new_format)
            }
        )

        future = publisher.publish(
            topic_path, data=message.data, **message.attributes)

        print(f"Published message: {future.result()}")
        return future.result()
