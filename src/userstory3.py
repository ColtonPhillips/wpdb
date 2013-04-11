# This is a user story hack jam by Colton Phillips for Pascal Courty.
# The location is Colton's house
# Apr 10 2013

# A User story is a
QUEST = """I want to use your wpdb module to create a csv file filled with 8 explicit properties on a list
of articles. The output must be formatted in a csv file for use with Stata software. """

import wpdb

def parse_args():
    import sys
    return sys.argv[1], sys.argv[2]
    
def user_story():
    try:        
    
    except Exception, e:
            print str(e)
            return False
    
    return False

def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
