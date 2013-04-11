# This is a user story hack jam by Colton Phillips for Pascal Courty.
# The location is Coltons basement
# MAR 1 2013

# A User story is a
QUEST = """I want to run your script and take my list of articles
to generate a CSV file populated with the properties I have given you."""

def parse_args():
    import sys
    return sys.argv[1], sys.argv[2]
    
def user_story():
    try:        
        import dummy
        import debug

        dummy_file, props_file = parse_args()
        dummy = dummy.generate_dummy_from_file(dummy_file)

        import wikiurl

        wf = wikiurl.WikiFetcher(dummy_file, props_file)

        wf.title = "Dance"
        wf.post()
        debug.dummy_xml_to_csv(wf.xml)
        debug.xml_to_file(wf.xml, "shmoutput.xml")
    
    except Exception, e:
            print str(e)
            return False
    
    return True

def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
