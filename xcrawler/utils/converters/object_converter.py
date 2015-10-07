
from xcrawler.utils import string_utils
from xcrawler.utils.converters.string_converter import StringConverter

class ObjectConverter:
    """Converts an instance of object to a specified type.

    """

    def __init__(self, string_converter=StringConverter()):
        self.string_converter = string_converter

    def convert_to_byte_string_utf8(self, o):
        string = self.convert_to_string(o)
        byte_string_utf8 = self.string_converter.convert_to_byte_string_utf8(string)
        return byte_string_utf8

    def convert_to_unicode_string(self, o):
        string = self.convert_to_string(o)
        unicode_string = self.string_converter.convert_to_unicode_string(string)
        return unicode_string

    def convert_to_string(self, o):
        if not string_utils.is_byte_string(o):
            o = str(o)
        return o

    def convert_to_empty_string_if_none(self, o):
        if o is None:
            o = ""
        return o

    def list_convert_to_byte_string_utf8(self, list_objects):
        return [self.convert_to_byte_string_utf8(o) for o in list_objects]

    def list_convert_to_unicode_string(self, list_objects):
        return [self.convert_to_unicode_string(o) for o in list_objects]

    def list_convert_to_string(self, list_objects):
        return [self.convert_to_string(o) for o in list_objects]

