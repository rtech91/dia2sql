#!/usr/bin/python3

from sys import exit, argv
from diaparser.parser import DiaParser
from app.settings import AppSettings
from argparse import ArgumentParser

def main(argv):

    parser = ArgumentParser()
    parser.description = "Convert Dia RDBMS model to the specified SQL engine schema."
    parser.add_argument('-f', '--from-dia', metavar="FILE", required=True, help="Path to Dia file with RDBMS model.")
    parser.add_argument('-t', '--to-sql', metavar="FILE", required=True, help="Path to SQL file to be saved.")
    parser.add_argument('-d', '--db-system', metavar="RDBMS type", required=False, default='mysql', help="Preferred database management system.")
    args = parser.parse_args();

    settings: AppSettings = AppSettings()
    settings.dia_path = args.from_dia
    settings.sql_path = args.to_sql
    settings.sql_type = args.db_system
    
    dia = DiaParser(settings.dia_path)
    dia.saveSQL(settings.sql_path)

if __name__ == "__main__":
   main(argv[1:])