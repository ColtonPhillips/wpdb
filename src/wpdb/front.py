# TODO Maybe we want to be able to fetch articles via id, not just title
# TODO The object oriented nature seems brittle. Why not just functions (consider this)

import csv
import urllib
import debug
from bs4 import BeautifulSoup

class Fetcher(object):
    """
    Fetcher makes querying wikipedia easier. A Fetcher is initialized with a set
    of properties parsed from a csv file. The Fetcher object must be primed with a title
    and a language before it can use the query.
    
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
        self.soup = None
        self.continue_attrs = dict()

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

    def _build_soup(self):
        self.soup = BeautifulSoup(self.xml, 'lxml')

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

    def _continue_url(self, xml):
        """
        Results from wikimedia may contain continue query codes that must be placed inside of the url
        and re-queried in order to get more fields for lists. This method will return a modified url
        containing the continue queries
        """
        soup = BeautifulSoup(xml, 'lxml')
        for query_continue in soup.find_all('query-continue'):
            for content in query_continue.contents:
                for key,value in content.attrs.iteritems():
                    self.continue_attrs[key] = value

        modified_url = self.url
        for key,value in self.continue_attrs.iteritems():
            modified_url += str('&' + key.encode('ascii', 'ignore') + '=' + value.encode('ascii', 'ignore'))
            #print "key", key.encode('ascii','ignore'),"value", value.encode('ascii','ignore')

        """
        print self.title
        print soup.prettify()
        print "modified url"
        print modified_url
        print "conti"
        print self.continue_attrs
        print ""
        print ''
        """
        
        return modified_url
     
    def _has_continue_queries(self,xml):
        """
        Use regex to see if an xml string contains a continue query
        """

        import re
        pattern = r'<query-continue>'#.</query-continue>'
        prog = re.compile(pattern, flags=re.DOTALL)
        mo = prog.search(xml)
        if mo is None:
            return False
        else:
            return True
    
    def post(self):
        """
        Post is an atomic operation that builds a complete xml including all data that must be 
        acquired via continue queries based on the primed Fetcher properties.
        
        Side Effects:
            xml is a complete description of the query in question
            continue_attrs are built, and erased afterwards.
        """
        self._build_url()

        working_xml = urllib.urlopen(self.url).read()

        while (self._has_continue_queries(working_xml)):
            new_xml = urllib.urlopen(self._continue_url(working_xml)).read()
            working_xml = new_xml            

        self.xml = working_xml
        self.continue_attrs = None
        self.continue_attrs = dict()

        self._build_soup()
        
    def log(self, file_path=None):
        """
        Log Fetcher information. If no file_path is given, just print it.
        
        TODO: Output to valid xml
        """
        
        out_string = str(self.xml)
        out_string += "\n<!--"
        out_string += "Language: " + str(self.language)
        out_string += "\nTitle: " + str(self.title)
        out_string += "\nurl: " + str(self.url) 
        out_string += "-->\n\n"
        
        if file_path is None:
            print out_string
        else:
            with open(file_path, 'w') as file:
                file.write(out_string)