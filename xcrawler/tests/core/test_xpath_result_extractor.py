
import unittest
import mock

import xcrawler

class TestXPathResultExtractor(unittest.TestCase):

    def setUp(self):
        self.extractor = xcrawler.XPathResultExtractor
        
    def test_extract_no_arguments(self):
        mock_result = ["mock_result1", "mock_result2", "mock_result3"]
        result = self.extractor.extract(mock_result)
        self.assertEquals(result, mock_result)   
        
    @mock.patch.object(xcrawler.XPathResultExtractor, 'xpath_result_get_index')
    @mock.patch.object(xcrawler.XPathResultExtractor, 'xpath_result_strip')    
    def test_extract_all_arguments(self, mock_extract_result_strip, mock_extract_result_get_index):
        mock_result = ["mock_result1", "mock_result2", "mock_result3"]
        mock_index = 1
        mock_default_value = "Unknown"
        mock_strip = True
        self.extractor.extract(mock_result, mock_index, mock_default_value, mock_strip)
        
        mock_extract_result_get_index.assert_called_once()
        mock_extract_result_strip.assert_called_once()
        
    def test_xpath_result_get_index(self):
        mock_result = ["mock_result1", " mock_result2     ", "mock_result3;a;b;c"]
        mock_index = 1;
        mock_default_value = "Unknown"
        result = self.extractor.xpath_result_get_index(mock_result, mock_index, mock_default_value)
        self.assertEquals(result, mock_result[mock_index])

    def test_xpath_result_get_index_exception(self):
        mock_result = ["mock_result1", "mock_result2", "mock_result3"]
        mock_index = len(mock_result) + 1;
        mock_default_value = "Unknown"
        result = self.extractor.xpath_result_get_index(mock_result, mock_index, mock_default_value)
        self.assertEquals(result, mock_default_value)

    def test_xpath_result_strip(self):
        mock_result = mock.Mock();
        mock_result.return_value = " mock_result2     "
        mock_result.strip.return_value = "mock_result2"
        mock_strip_pattern = "None"
        result = self.extractor.xpath_result_strip(mock_result, mock_strip_pattern)
        self.assertEquals(result, mock_result.strip.return_value)
        
    def test_xpath_result_split(self):
        mock_result = mock.Mock();
        mock_result.return_value = "mock_result3;a;b;c"
        mock_split_pattern = ";"
        mock_result.split.return_value = "[mock_result3,a,b,c]"
        result = self.extractor.xpath_result_split(mock_result, mock_split_pattern)
        self.assertEquals(result, mock_result.split.return_value)
        
              
