# Colton uses these things to do debugs and prints.
# Some of these things should probably be moved into their modules when appropriate.

def xml_to_file(xml, file_path):
    """
    Given an xml string and an absolute path, save the xml to the file.
    """
    with open(file_path, 'w') as file:
        file.write(str(xml.read()))

# Created for User Story #1
def make_dummy_xml_files(dummy, file_path):
    import urllib

    for title in dummy:

        url = make_dummy_url('en', title)
        xml = urllib.urlopen(url)
    
        file = open(title + '_' + file_path, "w")
        file.write(str(xml.read()))
        file.close()

# Created for User Story #1
def make_dummy_url(language, title, ):
    url = ""
    url += "http://"
    url += language 
    url += ".wikipedia.org/w/api.php?"
    url += "action=query"
    url += "&format=xml"
    url += "&titles=" + title
    url += "|Talk:" + title
    #url += "&prop=info|revisions|categories|images"
    url += "&prop=images|extlinks|categories|info"

    url += "&inprop=protection"
    ## THIS DOESN"T WORK. YOU CANT USE MULTIPLE PROPS
    #url += "&prop=extlinks"
    
    #url += "&inprop=protection|url|readable|subjectid|watched" # info properties
    #url += "&rvprop=userid|ids|timestamp|user|flags|comment|size" # revision properties
    return url       
        
# Created for User Story #2
def dummy_xml_to_csv(xml):
    from bs4 import BeautifulSoup
    import csv

    soup = BeautifulSoup(xml)

    with open ('output.csv', 'wb') as csvfile:
        my_writer = csv.writer(csvfile, delimiter=",",
                        quotechar='"', quoting=csv.QUOTE_MINIMAL)

        my_writer.writerow(["Article","# of images", "# of ext links"])
        # Lets just get some of the properties we want
        my_writer.writerow(['Dance', len(soup.images), len(soup.extlinks)])