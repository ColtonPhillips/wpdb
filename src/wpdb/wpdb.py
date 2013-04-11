def csv_file_to_list(csv_file_path):
    """Converts a csv file_path to a list of strings
    >>> csv_file_to_list("test/csv_file_to_list_test.csv")
    ['Pascal', 'Is', 'Lacsap']
    """
    import csv
    out_list = []
    with open(csv_file_path, 'rb') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in csvreader:
            out_list.append(', '.join(row))
    return out_list   
    
def _main():
    import urllib
    xml = urllib.urlopen("http://stats.grok.se/en/latest30/A_Dangerous_Path")
    
    file = open ("out.txt", 'w')
    #file.write(str(xml.read()))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    _main()
