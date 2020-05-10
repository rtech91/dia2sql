from os import access, R_OK
from os.path import isfile, exists
from sys import exit
from xml.dom.minidom import parseString, Document
import gzip

class DiaParser:
    """Class for parsing the Dia RDBMS model.

    Attributes:
    
    __parsed_xml (Document) Document storage for parsed Dia XML contents.
    """

    __parsed_xml: Document

    def __init__(self, path_to_dia: str):
        """Check Dia file existance and readability

        Args:
            path_to_dia (str): path to *.dia file

        """
        if exists(path_to_dia) and isfile(path_to_dia) and access(path_to_dia, R_OK):
            diafile = gzip.open(path_to_dia, 'r')
            dia_xml_contents = diafile.read()
            self.__parsed_xml = parseString(dia_xml_contents)
        else:
            print("File \"{0}\" does not exist or not readable!\n".format(path_to_dia))
            exit(2)