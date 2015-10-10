
import unittest
import mock
try:
    from urlparse import ParseResult
except ImportError:
    from urllib.parse import ParseResult

from xcrawler.http.urls.url_splitter import UrlSplitter


class TestUrlSplitter(unittest.TestCase):

    def setUp(self):
        self.url_splitter = UrlSplitter()

    @mock.patch('xcrawler.http.urls.url_splitter.urlparse')
    @mock.patch.object(UrlSplitter, 'format_to_parsable_url')
    def test_parse_url(self, mock_format_to_parsable_url, mock_urlparse_function):
        mock_url = "test.com/link/to/example_page.html"
        mock_formatted_url = "//test.com/link/to/example_page.html"
        mock_format_to_parsable_url.return_value = mock_formatted_url
        mock_parsed_url = mock.create_autospec(ParseResult).return_value
        mock_urlparse_function.return_value = mock_parsed_url
        result = self.url_splitter.parse_url(mock_url)
        mock_urlparse_function.assert_called_once_with("//test.com/link/to/example_page.html")
        self.assertEquals(result, mock_parsed_url)

    @mock.patch.object(UrlSplitter, 'add_protocol_domain_separator')
    def test_format_to_parsable_url(self, mock_add_protocol_domain_separator):
        mock_url = "test.com/link/to/example_page.html"
        mock_add_protocol_domain_separator.return_value = "//test.com/link/to/example_page.html"
        result = self.url_splitter.format_to_parsable_url(mock_url)
        self.assertEquals(result, "//test.com/link/to/example_page.html")

    @mock.patch.object(UrlSplitter, 'is_domain')
    def test_add_protocol_domain_separator(self, mock_is_domain):
        mock_url = "test.com/link/to/example_page.html"
        mock_is_domain.return_value = True
        result = self.url_splitter.add_protocol_domain_separator(mock_url)
        self.assertEquals(result, "//test.com/link/to/example_page.html")

    @mock.patch('xcrawler.http.urls.url_splitter.re.match')
    def test_is_domain_argument_valid_domain(self, mock_match_function):
        mock_domain = "test.com"
        mock_sre_match = mock.Mock()
        mock_match_function.return_value = mock_sre_match
        result = self.url_splitter.is_domain(mock_domain)
        self.assertEquals(result, True)

    @mock.patch('xcrawler.http.urls.url_splitter.re.match')
    def test_is_domain_argument_invalid_domain(self, mock_match_function):
        mock_domain = "test,com"
        mock_match_function.return_value = None
        result = self.url_splitter.is_domain(mock_domain)
        self.assertEquals(result, False)

    def test_get_part_url(self):
        mock_parsed_url = mock.create_autospec(ParseResult).return_value
        mock_parsed_url.__str__ = "http://test.com/link/to/example_page.html"
        mock_pattern = "{uri.netloc}"
        mock_string_pattern = mock.create_autospec(mock_pattern).return_value
        mock_string_pattern.format.return_value = "test.com"
        result = self.url_splitter.get_part_url(mock_string_pattern, mock_parsed_url)
        mock_string_pattern.format(mock_parsed_url)
        self.assertEquals(result, "test.com")

    @mock.patch.object(UrlSplitter, 'parse_url')
    @mock.patch.object(UrlSplitter, 'get_part_url')
    def test_get_protocol(self, mock_get_part_url, mock_parse_url):
        mock_url = "http://test.com/link/to/example_page.html"
        mock_parse_result = mock.create_autospec(ParseResult).return_value
        mock_parse_url.return_value = mock_parse_result
        mock_get_part_url.return_value = "http"
        result = self.url_splitter.get_protocol(mock_url)
        self.assertEquals(result, "http")

    @mock.patch.object(UrlSplitter, 'parse_url')
    @mock.patch.object(UrlSplitter, 'get_part_url')
    def test_get_protocol(self, mock_get_part_url, mock_parse_url):
        mock_url = "http://test.com/link/to/example_page.html"
        mock_parse_result = mock.create_autospec(ParseResult).return_value
        mock_parse_url.return_value = mock_parse_result
        mock_get_part_url.return_value = "http"
        result = self.url_splitter.get_protocol(mock_url)
        self.assertEquals(result, "http")

    @mock.patch.object(UrlSplitter, 'parse_url')
    @mock.patch.object(UrlSplitter, 'get_part_url')
    def test_get_domain(self, mock_get_part_url, mock_parse_url):
        mock_url = "http://test.com/link/to/example_page.html"
        mock_parse_result = mock.create_autospec(ParseResult).return_value
        mock_parse_url.return_value = mock_parse_result
        mock_get_part_url.return_value = "test.com"
        result = self.url_splitter.get_domain(mock_url)
        self.assertEquals(result, "test.com")

    @mock.patch.object(UrlSplitter, 'parse_url')
    @mock.patch.object(UrlSplitter, 'get_part_url')
    def test_get_protocol_domain(self, mock_get_part_url, mock_parse_url):
        mock_url = "http://test.com/link/to/example_page.html"
        mock_parse_result = mock.create_autospec(ParseResult).return_value
        mock_parse_url.return_value = mock_parse_result
        mock_get_part_url.return_value = "http://test.com/"
        result = self.url_splitter.get_protocol_domain(mock_url)
        self.assertEquals(result, "http://test.com/")


