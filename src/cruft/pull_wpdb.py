import urllib
import sys
from bs4 import BeautifulSoup

usage_string = """
Usage:

To retrieve valid articles for the wpdb system a user must pull them first. 
You can either append or write over the file. 
The maximum we can search for at one time is 500 (maybe?)

python pull_wpdb.py outfile.txt sample_size [w/a]
"""

def play_with_soup(soup):
    # just gonna play around a bit
    glom = soup.find_all('langlinks')
    
    print len(glom)
    print glom[0]
    print glom[0].name
    print glom[0].contents[0]
    print glom[0].find('ll')['lang']
    print soup.langlinks.ll['lang']
    
    
    #for chince in glom:
     #   print len(glom)
      #  print chince.encode('ascii', 'ignore') 
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
    
    url = "http://en.wikipedia.org/w/api.php?action=query&format=xml&generator=random&grnlimit=10&prop=langlinks"
    #url = "http://en.wikipedia.org/w/api.php?action=query&list=random&rnlimit=5"
    
    xml = urllib.urlopen(url)
    
    soup = BeautifulSoup(xml, 'lxml')
    #print (soup.prettify().encode('ascii', 'ignore'))
    play_with_soup(soup)   
if __name__ == "__main__":
    main()