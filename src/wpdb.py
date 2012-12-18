# TODO: Copy over code from nanda2.py - CP
# TODO: Which modules will you need to create? - CP
# TODO: What is the console interface?
# TODO: Password is in plain-text - CP
import MySQLdb
import sys

def main():
    try:
        conn = MySQLdb.connect(
                    #localhost
                    host    = "127.0.0.1",
                    user    = "root",
                    passwd  = "dangermouse",
                    db      = "wpdb")
    except MySQLdb.Error, e:
        print (e)
        sys.exit(1)


if __name__ == "__main__":
    main()
