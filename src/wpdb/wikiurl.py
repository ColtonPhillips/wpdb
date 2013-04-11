class WikiFetcher(object):

    def __init__(self, sample_file, props_file):
        self.url = ""
        self.language = "en"
        self.title = "Dummy_data"

        # e.g. ["prop=images|extlinks|categories|info", "inprop=protection"]
        self.properties = []
        
        self.xml = ""

        self.construct_property_rows(props_file)
        self.build_url()
        return

    def construct_property_rows(self, props_file):
        import csv
        with open(props_file, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                # Create a string w list elements seperated by | symbols
                row_string = '|'.join(row)

                # Now remove all the spaces!
                row_string = row_string.replace(' ', '')

                # Then find the first | and replace it with =
                row_string = row_string.replace('|', '=', 1)

                self.properties.append(row_string)
        return

    def build_url(self):
        self.url = ""
        self.url += "http://"
        self.url += self.language 
        self.url += ".wikipedia.org/w/api.php?"
        self.url += "action=query"
        self.url += "&format=xml"
        self.url += "&titles=" + self.title

        for prop in self.properties:
            self.url += "&" + prop

        return


    def post(self):
        self.build_url()

        import urllib
        self.xml = urllib.urlopen(self.url)

        # TODO: This has to be recursively built using query-continue


"""
# a dang dummy function!
def make_url(language, title, ):
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

"""