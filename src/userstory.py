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
        import dummy
        dummy = dummy.generate_dummy_from_file(dummy_file)
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
