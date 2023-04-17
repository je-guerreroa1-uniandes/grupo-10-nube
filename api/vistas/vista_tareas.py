import os
from flask import request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from flask_restful import Resource
from werkzeug.utils import secure_filename
# Celery for message broking
from datetime import datetime
from celery import Celery
from modelos import db, Usuario, UsuarioSchema, File, FileSchema

file_schema = FileSchema()

celery_app = Celery(__name__, broker='redis://:lOGleSPirDOLEYsiceWlemPtO@10.130.13.4:6379/0')
@celery_app.task(name='proccess_file')
def proccess_file(*args):
    pass

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
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


        # check if the post request has the file part
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        filenameParts = file.filename.split('.')
        filename = file.filename
        extension = filenameParts[-1]
        # f'Filename: {filename}, extension: {extension}'

        new_file = File(
            filename=filename,
            to_extension=destination_format,
            processed_filename='',
            state='UPLOADED',
            user_id=current_user['id'],
            datetime=datetime.utcnow()
        )
        db.session.add(new_file)
        db.session.commit()

        response_string = {'mensaje': 'tarea creada exitosamente', 'file': file_schema.dump(new_file)}
        # Call to message broker for queue the file
        args = (new_file.id, filename, destination_format, datetime.utcnow())
        result = proccess_file.apply_async(args=args, queue='files')
        task_id = result.id
        print(f'New task id {task_id} file_id: {new_file.id} datetime: {datetime.utcnow()}')

        return response_string, 200
