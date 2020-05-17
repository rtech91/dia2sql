#!/usr/bin/python3

from sys import exit, argv
from getopt import getopt, GetoptError
from diaparser.parser import DiaParser
from app.settings import AppSettings

def show_help():
    """Show app usage help information"""

    print ("""
        \rOVERVIEW: Convert Dia RDBMS model to the specified SQL engine schema.\n
        \rUSAGE: dia2sql --from-dia <*.dia file> --to-sql <*.sql file>\n\n
        \rOPTIONS:
        \r  -h, --help\t\t Show help information.
        \r  -f, --from-dia\t Path to Dia file with RDBMS model.
        \r  -t, --to-sql\t\t Path to SQL file to be saved.
    """)

def main(argv):
    try:
        # try to parse arguments from command line
        opts, args = getopt(argv, 'hf:t:', ['--help', '--from-dia', '--to-sql'])
    except getopt.GetoptError:
        show_help()
        exit(2)

    settings: AppSettings = AppSettings()

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            show_help()
            exit()
        elif opt in ("-f", "--dia-model"):
            settings.dia_path = arg
        elif opt in ("-t", "--to-sql"):
            settings.sql_path = arg
    
    del opts, args
    
    # if some arguments are empty, forcely show help information
    if settings.dia_path == '' or settings.sql_path == '':
        show_help()
        exit()

    dia = DiaParser(settings.dia_path)

if __name__ == "__main__":
   main(argv[1:])