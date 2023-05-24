import unittest
import tempfile
import os
import shutil

from jobs.file_converter import FileConverter


class FileConverterTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temp_dir)

    def test_to_zip(self):
        # Create a temporary file for testing
        test_file = os.path.join(self.temp_dir, 'test_file.txt')
        with open(test_file, 'w') as file:
            file.write('Test data')

        # Convert the file to zip format
        zip_file = FileConverter.to_zip(test_file, self.temp_dir)

        # Assert that the zip file was created
        self.assertTrue(os.path.exists(zip_file))

    def test_to_tar_gz(self):
        # Create a temporary file for testing
        test_file = os.path.join(self.temp_dir, 'test_file.txt')
        with open(test_file, 'w') as file:
            file.write('Test data')

        # Convert the file to tar.gz format
        tar_gz_file = FileConverter.to_tar_gz(test_file, self.temp_dir)

        # Assert that the tar.gz file was created
        self.assertTrue(os.path.exists(tar_gz_file))

    def test_to_tar_bz2(self):
        # Create a temporary file for testing
        test_file = os.path.join(self.temp_dir, 'test_file.txt')
        with open(test_file, 'w') as file:
            file.write('Test data')

        # Convert the file to tar.bz2 format
        tar_bz2_file = FileConverter.to_tar_bz2(test_file, self.temp_dir)

        # Assert that the tar.bz2 file was created
        self.assertTrue(os.path.exists(tar_bz2_file))

if __name__ == '__main__':
    unittest.main()