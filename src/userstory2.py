# This is a user story hack jam by Colton Phillips for Pascal Courty.
# The location is Coltons basement
# MAR 1 2013

# A User story is a
QUEST = """I want to run your script and take my list of articles
to generate a CSV file populated with the properties I have given you."""

# TODO We gotta get all the good stuff that pascal likes :3 DATA! DO YOU READ ME?

def parse_args():
    import sys
    return sys.argv[1]
    
def user_story():
    try:        
        import dummy
        import debug

        dummy_file = parse_args()
        dummy = dummy.generate_dummy_from_file(dummy_file)
        debug.yield_xml(dummy)
    
    except Exception, e:
            print(type(e), "%s") % e
            return False
    
    return False


def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
