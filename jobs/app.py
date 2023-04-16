import zipfile
import tarfile
import os
from celery import Celery

celery_app = Celery(__name__, broker='redis://localhost:6379/0')

def to_zip(file_path, destination_path):
    with zipfile.ZipFile(destination_path + '.zip', 'w') as zip_file:
        zip_file.write(file_path)

def to_tar_gz(file_path, destination_path):
    with tarfile.open(destination_path + '.tar.gz', 'w:gz') as tar:
        print(f'file url{file_path}')
        tar.add(file_path, arcname=os.path.basename(file_path))

def to_tar_bz2(file_path, destination_path):
    with tarfile.open(destination_path + '.tar.bz2', 'w:bz2') as tar:
        tar.add(file_path, arcname=os.path.basename(file_path))

@celery_app.task(name='proccess_file')
def proccess_file(filename, new_format, fecha):
    UPLOAD_FOLDER = './uploads'
    PROCESS_FOLDER = './processed'
    filenameParts = filename.split('.')

    log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log_conversion.txt')
    with open(log_file_path, 'a+') as file:
        file.write('{} to {} - solicitud de conversion: {}\n'.format(filename, new_format, fecha))

    formats = {
        'zip': to_zip,
        'tar_gz': to_tar_gz,
        'tar_bz2': to_tar_bz2
    }

    if new_format in formats.keys():
        print(f"calling {new_format}")
        func = formats[new_format]
        print(f"function: {func}")
        func(os.path.join(UPLOAD_FOLDER, filename), os.path.join(PROCESS_FOLDER, filenameParts[0]))
        print(f"destination: {os.path.join(PROCESS_FOLDER, filename)}")
    else:
        print("Invalid format")