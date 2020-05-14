from os import access, R_OK
from os.path import isfile, exists
from sys import exit
from lxml import etree
from gzip import open
from re import sub

class DiaParser:
    """Class for parsing the Dia RDBMS model.

    Attributes:
    
    __parsed_xml (Document) Document storage for parsed Dia XML contents.
    """

    __parsed_xml: bytes = ''

    def __init__(self, path_to_dia: str):
        """Check Dia file existance and readability

        Args:
            path_to_dia (str): path to *.dia file

        """
        if exists(path_to_dia) and isfile(path_to_dia) and access(path_to_dia, R_OK):
            diafile = open(path_to_dia, 'r')
            dia_xml_contents = diafile.read()
            del diafile
        else:
            print("File \"{0}\" does not exist or not readable!\n".format(path_to_dia))
            exit(2)
        
        if(self.__is_database(dia_xml_contents)):
            dia_xml_contents = self.__clear_dia_namespace(dia_xml_contents)
            self.__parsed_xml = etree.fromstring(dia_xml_contents)
        else:
            print("Given Dia file is not a database model, parsing will be aborted.")
        
        self.__collect_tables()

    def __is_database(self, dia_contents: bytes) -> bool:
        """Check does parsed Dia document is a Database"""
        return (str(dia_contents).count('Database') > 0)
    
    def __clear_dia_namespace(self, dia_contents: bytes) -> bytes:
        """Remove unnecessary Dia namespace additions."""
        return sub('(\sxmlns:dia="(.*)")|(dia:)', "", dia_contents.decode('utf8')).encode('utf8')

    def __collect_tables(self):
        """Find table objects in the given Dia model, and create entities for them."""
        layer = self.__parsed_xml.find('layer')
        for table_object in layer.findall('object[@type="Database - Table"]'):
            parsed_table_data = {}
            parsed_table_data['name'] = table_object.find('attribute[@name="name"]/string').text
            table_columns = table_object.findall('attribute[@name="attributes"]/composite[@type="table_attribute"]')
            parsed_table_data['columns']: list = []
            for column_object in table_columns:
                col_name = column_object.find('attribute[@name="name"]/string').text.replace('#', '')
                col_type = column_object.find('attribute[@name="type"]/string').text.replace('#', '')
                col_comment = column_object.find('attribute[@name="comment"]/string').text.replace('#', '')
                col_is_primary = column_object.find('attribute[@name="primary_key"]/boolean').get('val').replace('#', '')
                col_is_null = column_object.find('attribute[@name="nullable"]/boolean').get('val').replace('#', '')
                col_is_unique = column_object.find('attribute[@name="unique"]/boolean').get('val').replace('#', '')
                col_default_value = column_object.find('attribute[@name="default_value"]/string').text.replace('#', '')
                parsed_table_data['columns'].append({
                    'name': col_name,
                    'type': col_type,
                    'comment': col_comment,
                    'is_primary': col_is_primary,
                    'is_null': col_is_null,
                    'is_unique': col_is_unique,
                    'default_value': col_default_value
                })
            #TODO implement creating the table