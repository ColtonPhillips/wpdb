# Colton uses these things to do debugs and prints.
# Some of these things should probably be moved into their classes when appropriate.

# Created for User Story #1
def yield_xml(dummy):
    import urllib
    import wikiurl

    for title in dummy:

        url = wikiurl.make_url('en', title)
        xml = urllib.urlopen(url)
    
        out_file = "working/" + title + ".xml"
        file = open(out_file, "w")
        file.write(str(xml.read()))
        file.close()

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