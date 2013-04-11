# This is a user story hack jam by Colton Phillips for Pascal Courty.
# The location is Colton's basement
# MAR 1 2013

# A User story is a
QUEST = """I want to run your script and take my list of articles
to generate a CSV file populated with the properties I have given you."""

import wpdb

def parse_args():
    import sys
    return sys.argv[1], sys.argv[2]
    
def user_story():
    try:        
        dummy_file, props_file = parse_args()
        wf = wpdb.wikiurl.WikiFetcher(dummy_file, props_file)
        wf.title = "Dance"
        wf.post()
        wpdb.debug.dummy_xml_to_csv(wf.xml)
    
    except Exception, e:
            print str(e)
            return False
    
    return True

def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
