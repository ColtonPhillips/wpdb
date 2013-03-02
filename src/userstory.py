# This is a user story hack jam by Colton Phillips for Pascal Courty.
# The location is Tim Hortons in Victoria BC 
# FEB 18 2013

# A User story is a
QUEST = """I want to run your script and take my list of articles 
so I can make speculations about how people organize themselves
within wikipedia"""                                 # Pascal Courty

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
            print("%s") % e
            return False
    
    return True

def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
