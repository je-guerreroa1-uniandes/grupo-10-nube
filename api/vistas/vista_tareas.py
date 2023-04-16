# ZIP, 7Z, TAR.GZ, TAR.BZ2

import os
from flask import request
from flask import send_from_directory
from flask_restful import Resource
from werkzeug.utils import secure_filename
# Celery for message broking
from datetime import datetime
from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')
@celery_app.task(name='proccess_file')
def proccess_file(*args):
    pass

def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class VistaCreateTasks(Resource):

    def post(self):
        UPLOAD_FOLDER = './uploads'
        PROCESS_FOLDER = './processed'
        destination_format = request.form.get("to_format")
        print(f'to format -> {destination_format}')


        # check if the post request has the file part
        if 'file' not in request.files:
            # flash('No file part')
            return 'No file part'#redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            # flash('No selected file')
            return 'No selected file'# redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            #return redirect(url_for('download_file', name=filename))
            # return url_for('download_file', name=filename)

        filenameParts = file.filename.split('.')
        filename = file.filename
        extension = filenameParts[-1]
        response_string = f'Filename: {filename}, extension: {extension}'

        # Call to message broker for queue the file
        args = (filename, destination_format, datetime.utcnow())
        result = proccess_file.apply_async(args=args, queue='files')
        task_id = result.id
        print(f'New task id {task_id} {datetime.utcnow()}')


        return response_string, 200