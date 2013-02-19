# This is a user story hack jam by Colton Phillips for Pascal Courty.
# The location is Tim Hortons in Victoria BC 
# FEB 18 2013

# A User story is a
QUEST = """I want to run your script and take my list of articles 
so I can make speculations about how people organize themselves
within wikipedia"""                                 # Pascal Courty

# CONCEPTS:
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

def parse_args():
    import sys
    return sys.argv[1]

def generate_dummy_from_file(dummy_file):
    file = open(dummy_file, 'r')
    dummy = []
    for line in file:
        dummy.append(line.replace("\n",""))
    
    return dummy

# TODO: This is pre-baked. How do we get the flexibility we need? - CP
# TODO: Is there really no way to put those unary operations on new lines? - CP
def make_url(language, title, ):
    url = "http://" + language + ".wikipedia.org/w/api.php?action=query&format=xmlfm&titles=" + title + "&prop=info|revisions|categories&inprop=protection|url|readable|subjectid|watched&rvprop=userid|ids|timestamp|user|flags|comment|size"
    return url
    
def yield_xml(dummy):
    import urllib
    
    for title in dummy:
        url = make_url('en', title)
        xml = urllib.urlopen(url)
    
        out_file = title + ".xml"
        file = open(out_file, "w")
        file.write(str(xml.read()))
        file.close()
    
def user_story():
    try:        
        dummy_file = parse_args()
        dummy = generate_dummy_from_file(dummy_file)
        yield_xml(dummy)
    
    except Error, e:
            print("%s") % e
            return False
    
    return True

def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
