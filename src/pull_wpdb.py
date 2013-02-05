import urllib
import sys
from bs4 import BeautifulSoup


#TODO: Allow replace and append options. - CP
#TODO: Perhaps at one point this step is abstracted into the system. - CP
#TODO: Hey Tom Gibson I vaguely remember someone improving on sys args w/ some library? Curious. - CP

usage_string = """
Usage:

To retrieve valid articles for the wpdb system a user must pull them first. 
You can either append or write over the file. 
The maximum we can search for at one time is 500.

python pull_wpdb.py outfile.txt sample_size [w/a]
"""

def main():

    # Usage
    if (len(sys.argv) == 1):
        print usage_string
        sys.exit(1)
    out_file, sample_size = sys.argv[1], sys.argv[2]
    mode = 'a' #default to append
    if (len(sys.argv) >= 4):
        write_mode = sys.argv[3]
    
    # TODO: get sample_size random files.
    # TODO: Put the results in a file. 
    # TODO: Feel good about your accomplishments
    
    url = "http://en.wikipedia.org/w/api.php?action=query&format=xml&list=random&rnlimit=5&prop=info|revisions|categories&inprop=protection|url|readable|subjectid|watched&rvprop=userid|ids|timestamp|user|flags|comment|size&rvdir=older&clprop=timestamp"
    #url = "http://en.wikipedia.org/w/api.php?action=query&list=random&rnlimit=5"
    
    print url
    xml = urllib.urlopen(url)
    
    soup = BeautifulSoup(xml, 'lxml')
    #file = open(out_file, write_mode)
    #file.write(str(xml.read()))
    #file.close()
    print(soup.prettify())
        
if __name__ == "__main__":
    main()