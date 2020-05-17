import gzip
from os import access, R_OK
from os.path import isfile, exists
from sys import exit
from lxml import etree
from re import sub
from app.settings import AppSettings
from sqlgen.table import TableFactory, TableInterface
from collections import deque

class DiaParser:
    """Class for parsing the Dia RDBMS model.

    Attributes:
    
    __parsed_xml (bytes) Storage for parsed Dia XML contents.
    """

    __parsed_xml: bytes = ''

    # use deque() as much faster FIFO collection provider
    __tables: [TableInterface] = deque() 

    def __init__(self, path_to_dia: str):
        """Check Dia file existance and readability.

        Args:
            path_to_dia (str): path to *.dia file

        """
        if exists(path_to_dia) and isfile(path_to_dia) and access(path_to_dia, R_OK):
            diafile = gzip.open(path_to_dia, 'r')
            dia_xml_contents = diafile.read()
            del diafile
        else:
            print("File \"{0}\" does not exist or not readable!\n".format(path_to_dia))
            exit(2)
        
        if(self.__is_database(dia_xml_contents)):
            dia_xml_contents = self.__clear_dia_namespace(dia_xml_contents)
            self.__parsed_xml = etree.fromstring(dia_xml_contents)
        else:
            print("Specified Dia file is not a database model, parsing will be aborted.")
        
        self.__collect_tables()
    
    def saveSQL(self, path_to_sql: str):
        if len(self.__tables) > 0:
            droptable_list: str = ''
            sql_schema: str = ''

            #TODO: make droplist optional
            for i in range(len(self.__tables)):
                if(self.__tables[i] is not None):
                    droptable_list += "DROP TABLE `{table_name}`;\n".format(table_name=self.__tables[i].name);

            sql_schema += droptable_list + "\n\n"; 
            while self.__tables:
                table: TableInterface = self.__tables.popleft()
                if table is not None:
                    sql_schema += table.getSQL()
            sql_file = open(path_to_sql, 'w')
            sql_file.write(sql_schema)
            sql_file.close()

    def __is_database(self, dia_contents: bytes) -> bool:
        """Check is the parsed Dia document is a Database"""
        return (str(dia_contents).count('Database') > 0)
    
    def __clear_dia_namespace(self, dia_contents: bytes) -> bytes:
        """Remove unnecessary Dia namespace additions."""
        return sub('(\sxmlns:dia="(.*)")|(dia:)', "", dia_contents.decode('utf8')).encode('utf8')

    def __collect_tables(self):
        """Find table columns and properties in the given Dia model, and create entities for them."""
        layer = self.__parsed_xml.find('layer')
        for table_object in layer.findall('object[@type="Database - Table"]'):
            table_factory = TableFactory()
            parsed_table_data = {}
            parsed_table_data['name'] = table_object.find('attribute[@name="name"]/string').text.replace('#', '')
            parsed_table_data['comment'] = table_object.find('attribute[@name="comment"]/string').text.replace('#', '')
            table_columns = table_object.findall('attribute[@name="attributes"]/composite[@type="table_attribute"]')
            parsed_table_data['columns'] = deque()
            for column_object in table_columns:
                parsed_table_data['columns'].append({
                    'name': column_object.find('attribute[@name="name"]/string').text.replace('#', ''),
                    'type': column_object.find('attribute[@name="type"]/string').text.replace('#', ''),
                    'comment': column_object.find('attribute[@name="comment"]/string').text.replace('#', ''),
                    'is_primary': column_object.find('attribute[@name="primary_key"]/boolean').get('val').replace('#', ''),
                    'is_null': column_object.find('attribute[@name="nullable"]/boolean').get('val').replace('#', ''),
                    'is_unique': column_object.find('attribute[@name="unique"]/boolean').get('val').replace('#', ''),
                    #TODO: add support of default type
                    #'default_value': column_object.find('attribute[@name="default_value"]/string').text.replace('#', '')
                })
            self.__tables.append( table_factory.get_table(parsed_table_data) )