import merge_xml
import csv
import urllib
import debug
import re
from bs4 import BeautifulSoup

class Fetcher(object):
    """
    A Fetcher makes getting XML data from Wikipedia. It builds a URL based on
    customizable CSV property files and handles the continue query process.
    """

    def __init__(self, props_file_path, title=None, language='en'):
        
        # Input
        self.language = language
        self.title = title
        self.url = None
        self.properties = None
        self.continue_attrs = dict()

        # Output
        self.xml = None
        self.soup = None

        # Fetch
        self.construct_property_rows(props_file_path)
        self._build_url()
        self._post()
        self._build_soup()

    def construct_property_rows(self, props_file_path):
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
        with open(props_file_path, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row in reader:
                row_string = '|'.join(row)
                row_string = row_string.replace(' ', '')
                row_string = row_string.replace('|', '=', 1)

                self.properties.append(row_string)

    def _build_url(self):
        """
        Builds url field before query Wikimedia. 
        """
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
            
        return modified_url
     
    def _has_continue_queries(self,xml):
        """
        Use regex to see if an xml string contains a continue query
        """
        pattern = r'<query-continue>'
        prog = re.compile(pattern, flags=re.DOTALL)
        mo = prog.search(xml)
        if mo is None: return False 
        else: return True
    
    def _post(self):
        """
        Post builds a complete xml including all data that must be 
        acquired via continue queries.
        """
        working_xml = urllib.urlopen(self.url).read()

        while (self._has_continue_queries(working_xml)):
            new_xml = urllib.urlopen(self._continue_url(working_xml)).read()
            wang_xml = working_xml
            merge_xml.xml_merge(working_xml, new_xml)
            if (working_xml == wang_xml or working_xml ==new_xml):
                print "borked"

        self.xml = working_xml

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


    def _build_soup(self):
        self.soup = BeautifulSoup(self.xml, 'lxml')