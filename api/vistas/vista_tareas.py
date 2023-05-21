import json
import os
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import secure_filename
# Celery for message broking
from datetime import datetime
from google.cloud import pubsub_v1
from modelos import db, Usuario, UsuarioSchema, File, FileSchema
import config
from google.cloud import storage
from google.oauth2 import service_account

file_schema = FileSchema()

# Create credentials using the service account key
credentials = service_account.Credentials.from_service_account_file(
    config.G10_SERVICE_ACCOUNT_KEY_PATH,
    scopes=['https://www.googleapis.com/auth/cloud-platform']
)

# Create a client instance with the specified service account key
client = storage.Client.from_service_account_json(config.G10_SERVICE_ACCOUNT_KEY_PATH)

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
            File.user_id==current_user['id']
        ).all()
        return [file_schema.dump(file) for file in files]

        # return {'mensaje': 'tarea creada exitosamente', 'usuario': current_user}

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        UPLOAD_FOLDER = './uploads'
        PROCESS_FOLDER = './processed'
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
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

        filenameParts = file.filename.split('.')
        filename = file.filename
        extension = filenameParts[-1]

        # Create a blob name with a unique identifier and file extension
        blob_name = f"{current_user['id']}/{filenameParts[0]}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.{extension}"
        blob = bucket.blob(blob_name)

        # Assuming you have a cloud store object called "blob"
        folder_path = "general/uploads/"  # Specify the desired folder path
        destination_path = folder_path + filename
        # Upload the file to Google Cloud Storage
        blob.upload_from_filename(file_path, destination_path)

        new_file = File(
            filename=secure_filename(file.filename),
            to_extension=destination_format,
            processed_filename='',
            state='UPLOADED',
            user_id=current_user['id'],
            created_at=datetime.utcnow()
        )
        db.session.add(new_file)
        db.session.commit()

        response_string = {'mensaje': 'tarea creada exitosamente', 'file': file_schema.dump(new_file)}

        # Call the message broker for queuing the file
        args = (new_file.id, filename, destination_format)
        message = {
            'file_id': new_file.id,
            'filename': filename,
            'destination_format': destination_format
        }
        message_data = json.dumps(message).encode('utf-8')

        topic_path = publisher.topic_path(config.GOOGLE_PUBSUB_PROJECT_ID, config.GOOGLE_PUBSUB_TOPIC_NAME)
        future = publisher.publish(topic_path, data=message_data)
        message_id = future.result()
        print(f'Published message with ID: {message_id}')

        return response_string, 200
