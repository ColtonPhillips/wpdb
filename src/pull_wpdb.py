import MySQLdb
import sys

#TODO: Allow replace and append options. - CP
#TODO: Perhaps at one point this step is abstracted into the system. - CP
#TODO: Hey Tom Gibson I vaguely remember someone improving on sys args w/ some library? Curious. - CP

usage_string = """
Usage:

To retrieve valid articles for the wpdb system a user must pull them first. 
You can either append or write over the file. 

python pull_wpdb.py outfile.txt sample_size [-r/-a]
"""

#TODO: Copy Paste Code Antipattern - CP
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

    # Usage
    if (len(sys.argv) == 1):
        print usage_string
        sys.exit(1)
    out_file, sample_size = sys.argv[1], sys.argv[2]
    mode = '-a' #default to append
    if (len(sys.argv) >= 4):
        mode = sys.argv[3]

    db = connect_to_database()
    
    print out_file, sample_size, mode
        
if __name__ == "__main__":
    main()