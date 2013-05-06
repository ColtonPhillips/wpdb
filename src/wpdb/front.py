import lxml.etree
import merge_xml
import csv
import urllib
import debug
#from bs4 import BeautifulSoup
 
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
        self._build_tree()
        #self._build_soup()
 
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
        base_url = "http://{0}.wikipedia.org/w/api.php?action=query&format=xml&titles={1}"
        self.url = base_url.format(self.language, self.title)
        
        for prop in self.properties:
            self.url += "&" + prop
 
    def _continue_url(self, xml):
        """
        Results from wikimedia may contain continue query codes that must be placed inside of the url
        and re-queried in order to get more fields for lists. This method will return a modified url
        containing the continue queries
        """
        tree = lxml.etree.fromstring(xml)
        for query_continue in tree.findall('query_continue'):
            #For each subelement, get each attribute
            for query_subelement in query_continue:
                for key in query_subelement.attrib.keys():
                    self.continue_attrs[key] = query_subelement.attrib[key]
            
        #soup = BeautifulSoup(xml, 'lxml')
        #for query_continue in soup.find_all('query-continue'):
        #    for content in query_continue.contents:
        #        for key,value in content.attrs.iteritems():
        #            self.continue_attrs[key] = value
 
        modified_url = self.url
        for key,value in self.continue_attrs.iteritems():
            modified_url += str('&' + key.encode('ascii', 'ignore') + '=' + value.encode('ascii', 'ignore'))
            
        return modified_url
     
    def _has_continue_queries(self, xml):
        """
        Check the xml as string, for the substring <query-continue> to detect
        if there there will be further input
        """
        return r'<query-continue>' in xml
    
    def _post(self):
        """
        Post builds a complete xml including all data that must be 
        acquired via continue queries.
        """ 
        reference_xml = urllib.urlopen(self.url).read()
        
        while (self._has_continue_queries(reference_xml)):
            #Extracting the url for the next query, then reading the data
            new_xml = urllib.urlopen(self._continue_url(reference_xml)).read()

            #Create lxml structures for each: reference and new
            reference_elm =lxml.etree.fromstring(reference_xml)
            subject_elm = lxml.etree.fromstring(new_xml)

            #Remove the query-continue from the reference
            query_continue = reference_elm.find('query-continue')
            query_continue.getparent().remove(query_continue)

            #Merge the xml; nothing has been coereced to html
            merge_xml.xml_merge(reference_elm, subject_elm)
 
            #Pass the merged lxml tree back as a string as reference_xml
            reference_xml = str(lxml.etree.tostring(reference_elm, pretty_print=False, encoding='utf-8'))

        #Set self.xml to the final merged xml
        self.xml = reference_xml
 
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
 
 
    def _build_tree(self):
        self.tree = lxml.etree.fromstring(self.xml)
    #def _build_soup(self):
    #    self.soup = BeautifulSoup(self.xml, 'lxml')
