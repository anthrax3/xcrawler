
import unittest
import mock

from xcrawler.compatibility.compatibility_factory import CompatibilityFactory
from xcrawler.files.writers.file_writer_factory import FileWriterFactory


class TestCompatibilityFactory(unittest.TestCase):

    def setUp(self):
        self.factory = FileWriterFactory()

    @mock.patch.object(FileWriterFactory, 'create_item_writer_csv')
    def test_create_item_writer_based_on_file_extension_csv(self, mock_create_item_writer_csv):
        mock_file_name = "mock.csv"
        mock_item_writer = mock.Mock()
        mock_create_item_writer_csv.return_value = mock_item_writer
        result = self.factory.create_item_writer_based_on_file_extension(mock_file_name)
        self.assertEquals(result, mock_item_writer)

    def test_create_item_writer_based_on_file_extension_value_error(self):
        mock_file_name = "mock.exe"
        self.assertRaises(ValueError, self.factory.create_item_writer_based_on_file_extension, mock_file_name)

    @mock.patch.object(FileWriterFactory, 'create_object_writer_csv')
    def test_create_item_writer_csv(self, mock_create_object_writer_csv):
        mock_object_writer = mock.Mock()
        mock_create_object_writer_csv.return_value = mock_object_writer
        result = self.factory.create_item_writer_csv()
        self.assertEquals(result.object_writer, mock_object_writer)

    @mock.patch('xcrawler.files.writers.file_writer_factory.CompatibilityFactory')
    @mock.patch('xcrawler.files.writers.file_writer_factory.ObjectWriterCsv')
    def test_create_object_writer_csv(self, mock_object_writer_csv_class, mock_compatibility_factory_class):
        mock_factory = mock.create_autospec(CompatibilityFactory).return_value
        mock_file_opener = mock.Mock()
        mock_object_to_string_converter = mock.Mock()
        mock_object_writer = mock.Mock()

        mock_compatibility_factory_class.return_value = mock_factory
        mock_factory.create_compatible_file_opener_write.return_value = mock_file_opener
        mock_factory.create_compatible_object_string_converter.return_value = mock_object_to_string_converter
        mock_object_writer_csv_class.return_value = mock_object_writer
        result = self.factory.create_object_writer_csv()
        mock_object_writer_csv_class.assert_called_once_with(mock_file_opener, mock_object_to_string_converter)
        self.assertEquals(result, mock_object_writer)




