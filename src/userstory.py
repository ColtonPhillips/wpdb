# This is a user story hack jam by Colton Phillips for Pascal Courty.
# The location is Tim Hortons in Victoria BC

# A User story is a
QUEST = """I want to run your script and take my list of articles 
so I can make speculations about how people organize themselves
within wikipedia"""                                 # Pascal Courty

# TODO: Make a mildly formal definition of a dummy. Think about relational algebra
#           when you define it. It should almost act as a key to the exact article you are needing.
#           the dummy needs to be unicode friendly!

# TODO: We don't know the full functionality or purpose of the list
#           We are using to fuel the process. Let us give it a dummy 
#           name to make this fact clear. - CP
#                   sample

# Dummy formatting e.g.
"""
first_article_title
second_article_title
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
    
def user_story():
    dummy_file = parse_args()
    dummy = generate_dummy_from_file(dummy_file)
    
    print dummy
    return False

def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
