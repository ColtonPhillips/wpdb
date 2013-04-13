import csv
import urllib
import debug
        
class Fetcher(object):
    """
    Fetcher makes querying wikipedia easier. A Fetcher is initialized with a set
    of properties parsed from a csv file. The Fetcher must be initialized with a title
    and a language to query.
    
    Once a Fetcher is primed, call post() to send the query. The Fetcher object will
    hold a reference to the xml that is generated from the server.
    
    NOTE: It is assumed that for each wikimedia language specific database, a unique
        query is formed, though the xml that is returned may need to be handled in a unique way.
    """

    def __init__(self, props_file, language=None, title=None):
        
        self.language = language
        self.title = title
        self.url = None
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
                row_string = '|'.join(row)
                row_string = row_string.replace(' ', '')
                row_string = row_string.replace('|', '=', 1)

                self.properties.append(row_string)

    def _build_url(self):
        """
        Builds url field before posting to Wikipedia. 
        
        Side Effect:
            Sets url to properly formatted url based on input to Fetcher fields
        """
        if (self.language is None or self.title is None or self.properties is None):
            # TODO: What type of exception would this throw?
            print "Fetcher is not primed. Raises an exception, but for now it just crashes!"
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

    def _continue_url(continue_queries):
        """
        Results from wikimedia may contain continue query codes that must be placed inside of the url
        and re-queried in order to get more fields for lists. This method will return a modified url
        containing the continue queries
        """
        modified_url = self.url
        for query in continue_queries:
            modified_url += '&' + query
        return modified_url
     
    
    
    def post(self):
        """
        Post is an atomic operation that builds a complete xml including all data that must be 
        acquired via continue queries based on the primed Fetcher properties.
        
        Side Effects:
            xml is a complete description of the query in question
        """
        self._build_url()

        working_xml = urllib.urlopen(self.url)
        
        # TODO: This has to be recursively built using query-continue
        
        self.xml = working_xml.read()
        
        
        debug.xml_to_file(working_xml, "out/xml_1.xml")
        self.log("out/log.xml")
        
    def log(self, file_path=None):
        """
        Log Fetcher information. If no file_path is given, just print it.
        
        Gosh this code is gross.
        """
        
        out_string = str(self.xml)
        out_string += "\n<!--"
        out_string += "Language: " + str(self.language)
        out_string += "\nTitle: " + str(self.title)
        out_string += "\nurl: " + str(self.url) 
        out_string += "xml: -->\n\n"
        
        if file_path is None:
            print out_string
        else:
            with open(file_path, 'w') as file:
                file.write(out_string)