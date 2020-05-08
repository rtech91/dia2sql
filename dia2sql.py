#!/usr/bin/python
import sys, getopt

def show_help():
    """Show help in the terminal"""

    print ("""
        \rUsage: dia2sql [OPTIONS]\n\n
        \r-h --help\t\t show this help
        \r-f --from-dia\t\t path to Dia file with RDBMS model
        \r-t --to-sql\t\t path to SQL file to be saved
    """)

def main(argv):
    try:
        opts, args = getopt.getopt(argv, 'hf:t:', ['--help', '--from-dia', '--to-sql'])
    except getopt.GetoptError:
        show_help()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h' or opt == '--help':
            show_help()
            sys.exit()
        elif opt in ("-f", "--dia-model"):
            dia_model = arg
        elif opt in ("-t", "--to-sql"):
            outputfile = arg
    else:
        show_help()
        sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])