# This is a user story hack jam by Colton Phillips for Pascal Courty.
# The location is Colton's house
# Apr 10 2013

# A User story is a
QUEST = """I want to use your wpdb module to create a csv file filled with 8 explicit properties on a list
of articles. The output must be formatted in a csv file for use with Stata software. """

import wpdb

def test_crunch(xml):
    print ""

userstory3_crunches = [test_crunch]

def parse_args():
    import sys
    return (sys.argv[1], sys.argv[2])
 
def user_story():
    try:        
        articles_file_path, property_file_path = parse_args()
    
        articles = wpdb.csv_file_to_list(articles_file_path)
        wf = wpdb.front.Fetcher(property_file_path)
        wf.language = 'en'
        articles_xml = []
        print "Fetch articles"
        for article in articles:
            print "Fetching: " + article 
            wf.title = article
            wf.post()
            print "Done: " + article
            print ""
            articles_xml.append(wf.xml)

        cr = wpdb.middle.Cruncher()
        cr.addFunctions(userstory3_crunches)
        for article_xml in articles_xml:
            cr.xml = article_xml
            cr.crunch() # calls all functions and puts results in a list
            #print cr.result()

    except Exception, e:
            print str(e)
            return False
    
    return False

def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
