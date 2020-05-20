import unittest, os
from mediastack.utility.MediaIO import MediaIO

class TestMediaIOScanDirectory(unittest.TestCase):

    def create_test_file(self, file_path: str):
        some_file = open(file_path, "w")
        some_file.write("")
        some_file.close()

    def test_scan_emtpy_directory(self):
        self.assertEqual([], MediaIO.scan_directory("mediastack/tests/media/output"))

    def test_scan_directory_with_single_file(self):
        self.create_test_file("mediastack/tests/media/output/some_file.txt")
        expected = ["mediastack/tests/media/output/some_file.txt"]
        self.assertEqual(expected, MediaIO.scan_directory("mediastack/tests/media/output"))
        os.remove("mediastack/tests/media/output/some_file.txt")

    def test_scan_directory_with_subdirectory(self):
        expected = [
            "mediastack/tests/media/output/some_dir/some_file1.txt", 
            "mediastack/tests/media/output/some_dir/some_file2.txt", 
            "mediastack/tests/media/output/some_dir/some_file3.txt"
        ]

        os.mkdir("mediastack/tests/media/output/some_dir")
        for file in expected:
            self.create_test_file(file)

        result = MediaIO.scan_directory("mediastack/tests/media/output")

        for file in expected:
            os.remove(file)
        os.rmdir("mediastack/tests/media/output/some_dir")

        expected.sort()
        result.sort()
        self.assertEqual(expected, result)

    def test_scan_directory_with_file_and_subdirectory(self):
        expected = [
            "mediastack/tests/media/output/some_dir/some_file1.txt", 
            "mediastack/tests/media/output/some_dir/some_file2.txt", 
            "mediastack/tests/media/output/some_dir/some_file3.txt"
        ]

        os.mkdir("mediastack/tests/media/output/some_dir")
        for file in expected:
            self.create_test_file(file)
        self.create_test_file("mediastack/tests/media/output/some_file.txt")
        expected.append("mediastack/tests/media/output/some_file.txt")

        result = MediaIO.scan_directory("mediastack/tests/media/output")

        for file in expected:
            os.remove(file)
        os.rmdir("mediastack/tests/media/output/some_dir")

        expected.sort()
        result.sort()
        self.assertEqual(expected, result)
    
    def test_scan_non_existant_directory(self):
        with self.assertRaises(FileNotFoundError):
            MediaIO.scan_directory("non_existant_directory")