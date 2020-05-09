from os import access, R_OK
from os.path import isfile, exists
from sys import exit

class DiaParser:
    """Class for parsing the Dia RDBMS model.

    Attributes:
    
    __dia_path (str): Full path to *.dia file.
    """

    __dia_path = ''
    """Storage for full *.dia file path"""

    def __init__(self, path_to_dia: str):
        """Check Dia file existance and readability

        Args:
            path_to_dia (str): path to *.dia file

        """
        if exists(path_to_dia) and isfile(path_to_dia) and access(path_to_dia, R_OK):
            self.__dia_path = path_to_dia
        else:
            print("File \"{0}\" does not exist or not readable!\n".format(path_to_dia))
            exit(2)