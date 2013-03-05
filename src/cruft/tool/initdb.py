import MySQLdb
import sys

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
    
    # Create our database
    init_query = """ 
		DROP TABLE IF EXISTS test_table;
		"""	
    db.query(init_query)

if __name__ == "__main__":
    main()
