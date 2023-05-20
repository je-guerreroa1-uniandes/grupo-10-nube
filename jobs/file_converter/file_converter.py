import zipfile
import tarfile
import os
import zlib


class FileConverter:
    @staticmethod
    def to_zip(file_path, destination_path):
        processed_filename = destination_path + '.zip'
        with zipfile.ZipFile(processed_filename, mode='w', compression=zipfile.ZIP_DEFLATED, compresslevel=zlib.Z_BEST_COMPRESSION) as zip_file:
            zip_file.write(file_path)
        return processed_filename

    @staticmethod
    def to_tar_gz(file_path, destination_path):
        processed_filename = destination_path + '.tar.gz'
        with tarfile.open(destination_path + '.tar.gz', 'w:gz') as tar:
            print(f'file url{file_path}')
            tar.add(file_path, arcname=os.path.basename(file_path))
        return processed_filename

    @staticmethod
    def to_tar_bz2(file_path, destination_path):
        processed_filename = destination_path + '.tar.bz2'
        with tarfile.open(destination_path + '.tar.bz2', 'w:bz2') as tar:
            tar.add(file_path, arcname=os.path.basename(file_path))
        return processed_filename