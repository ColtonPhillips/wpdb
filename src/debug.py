# Colton uses these things to do debugs and prints.
# Some of these things should probably be moved into their classes when appropriate.

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