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

def generate_dummy_from_file(dummy_file):
    file = open(dummy_file, 'r')
    dummy = []
    for line in file:
        dummy.append(line.replace("\n",""))
    
    return dummy