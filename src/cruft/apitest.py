# I'll just use this one for testing - CP
# You can use a my_conv dict and pass that into the connect to auto convert some types - CP

import MySQLdb
import sys
import urllib

def main():
    try:
        db = MySQLdb.connect(
                    #localhost
                    host    = "127.0.0.1",
                    user    = "root",
                    passwd  = "dangermouse",
                    db      = "wpdb")
    except MySQLdb.Error, e:
        print(e)
        sys.exit(1)
        
    #db.query("""create table test_table(
     #           FartName varchar(255), 
      #          ShitName varchar(255)
       #         )""")
    
    db.query("""describe test_table""")
    
    r = db.store_result()
    
    print r.fetch_row(2)

"""    url = "http://en.wikipedia.org/w/api.php?action=query&format=xmlfm&titles=%s&prop=info|revisions|categories&inprop=protection|url|readable|subjectid|watched&rvprop=userid|ids|timestamp|user|flags|comment|size&rvdir=older&rvstart=%s000000&rvend=%s000000&rvlimit=%d&clprop=timestamp" % ("Dance", 20121231, 20010101, 400)

    xml = urllib.urlopen(url)
    
    file = open("temp.txt", "w")
    file.write(str(xml.read()))
    file.close()
    
"""
    
if __name__ == "__main__":
    main()