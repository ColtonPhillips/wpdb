import csv

class WikiFetcher(object):
    """
    WikiFetcher makes querying wikipedia easier. A WikiFetcher is initialized with a set
    of properties parsed from a csv file. The WikiFetcher must be initialized with a title
    and a language to query.
    
    Once a WikiFetcher is primed, call post() to send the query. The WikiFetcher object will
    hold a reference to the xml that is generated from the server.
    
    NOTE: It is assumed that for each wikimedia language specific database, a unique
        query is formed, though the xml that is returned may need to be handled in a unique way.
    """

    def __init__(self, props_file):
        self.url = None
        self.language = None
        self.title = None
        self.xml = None
        self.properties = None

        self.construct_property_rows(props_file)

    def construct_property_rows(self, props_file):
        """
        From a formatted csv file, set properties list.
            Format:
                property_1, value_1, ..., value_n
                property_2, value_1, ..., value_m
                    .
                    .
                    .
                property_n, value_1, ..., value_z
        
            Side Effect e.g.:
                properties = ["prop=images|extlinks|categories|info", "inprop=protection"]
        
        """
        self.properties = []
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

    def _build_url(self):
        """
        Builds url field before posting to Wikipedia. 
        
        Side Effect:
            Sets url to properly formatted url based on input to WikiFetcher fields
        """
        if (self.language is None or self.title is None or self.properties is None):
            # TODO: What type of exception would this throw?
            print "WikiFetcher is not primed. Raises an exception, but for now it just crashes!"
            import sys
            sys.exit()
        
        self.url = ""
        self.url += "http://"
        self.url += self.language 
        self.url += ".wikipedia.org/w/api.php?"
        self.url += "action=query"
        self.url += "&format=xml"
        self.url += "&titles=" + self.title

        for prop in self.properties:
            self.url += "&" + prop

    def post(self):
        self._build_url()

        import urllib
        self.xml = urllib.urlopen(self.url)

        # TODO: This has to be recursively built using query-continue