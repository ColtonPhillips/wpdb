# TODO: Copy over code from nanda2.py - CP
# TODO: Which modules will you need to create? - CP
# TODO: What is the console interface?
# TODO: Password is in plain-text - CP
# TODO: Perhaps a debug mode that uses a Profiler - CP

# one hour git setup files. created dirtree helper module

import MySQLdb
import sys
from dirtree import dirt

def connect_to_database():
    try:
        conn = MySQLdb.connect(
                    #localhost
                    host    = "127.0.0.1",
                    user    = "root",
                    passwd  = "dangermouse",
                    db      = "wpdb")
        return conn
    except MySQLdb.Error, e:
        print (e)
        sys.exit(1)

def main():
    db = connect_to_database()
    dirt(db)

if __name__ == "__main__":
    main()
