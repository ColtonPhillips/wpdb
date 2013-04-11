# Colton uses these things to do debugs and prints.
# Some of these things should probably be moved into their modules when appropriate.

def xml_to_file(xml, file_path):
    """
    Given an xml string and an absolute path, save the xml to the file.
    """
    with open(file_path, 'w') as file:
        file.write(str(xml.read()))

# Created for User Story #1
def make_dummy_xml_files(dummy, file_path):
    import urllib

    for title in dummy:

        url = make_dummy_url('en', title)
        xml = urllib.urlopen(url)
    
        file = open(title + '_' + file_path, "w")
        file.write(str(xml.read()))
        file.close()

# Created for User Story #1
def make_dummy_url(language, title, ):
    url = ""
    url += "http://"
    url += language 
    url += ".wikipedia.org/w/api.php?"
    url += "action=query"
    url += "&format=xml"
    url += "&titles=" + title
    url += "|Talk:" + title
    #url += "&prop=info|revisions|categories|images"
    url += "&prop=images|extlinks|categories|info"

    url += "&inprop=protection"
    ## THIS DOESN"T WORK. YOU CANT USE MULTIPLE PROPS
    #url += "&prop=extlinks"
    
    #url += "&inprop=protection|url|readable|subjectid|watched" # info properties
    #url += "&rvprop=userid|ids|timestamp|user|flags|comment|size" # revision properties
    return url       
        
# Created for User Story #2
def dummy_xml_to_csv(xml):
    from bs4 import BeautifulSoup
    import csv

    soup = BeautifulSoup(xml)

    with open ('output.csv', 'wb') as csvfile:
        my_writer = csv.writer(csvfile, delimiter=",",
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)

        my_writer.writerow(["Article","# of images", "# of ext links"])
        # Lets just get some of the properties we want
        my_writer.writerow(['Dance', len(soup.images), len(soup.extlinks)])
        
# Created for User Story #2
def generate_dummy_from_file(dummy_file):
    file = open(dummy_file, 'r')
    dummy = []
    for line in file:
        dummy.append(line.replace("\n",""))
    
    return dummy


# TODO get rid of this crap asap - overengineering - CP    
DUMMY_TYPE = """
We don't know the full functionality of the dummy,
so we make that perfectly clear by calling it as such.

A dummy is a structured file format (and generated runtime object)
that is input to an atomic WPDB system command.

Dummy syntax will be defined using test driven development,
proving system correctness and to accrete a suite of tests. 

    e.g.    >> wpdb.py branch our_database
            >> wpdb.py push dummy.dum

A dummy is a "candidate key" to a set of unique wikipedia articles. 
It provides symbolic links to these articles without describing
any of the processes which are acted on the dummy.

The purpose of the dummy is to create a layer of indirection between
WPDB and the user. This layer allows for sets of articles of interest
to be generated in a variety ways:
(human,human assisted by script or GUI, random, bot, portal/category scraping)

There should be no size restrictions on the dummy.
A workflow of creating and combining dummies enables
creative and powerful research. Advanced flags may
enable time saving measures. (--get-all-available-lang, -l 'en' 'fr')
"""

DUMMY_SYNTAX = """
article_title_in_english
article_title_in_english
"""