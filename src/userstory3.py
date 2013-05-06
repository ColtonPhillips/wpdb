from pprint import pprint as pp

# This is a user story hack jam by Colton Phillips for Pascal Courty.
# The location is Colton's house
# Apr 10 2013

# A User story is a
QUEST = """I want to use your wpdb module to create a csv file filled with 8 explicit properties on a list
of articles. The output must be formatted in a csv file for use with Stata software. """

import wpdb
import traceback
import lxml.etree

def xml_len(data):
    xml = data['xml']
    return "XML length: " + str(len(xml))

def tree_len(data):
    tree = data['tree']
    return "Tree length: " + str(len(tree))

def daily_views_last_month(data):
    import urllib, re
    website = urllib.urlopen("http://stats.grok.se/en/latest30/" + str(data['title'])).read()
    pattern = r'(?<=viewed )\d*'
    prog = re.compile(pattern)
    match_object = prog.search(website)
    return "Views in last month: " + str(match_object.group(0)) 

userstory3_crunches = [tree_len, xml_len, daily_views_last_month]

def parse_args():
    import sys
    return (sys.argv[1], sys.argv[2])
 
def user_story():
    articles_xml = []
    articles_file_path, property_file_path = parse_args()
    articles = wpdb.csv_file_to_list(articles_file_path)
    for article in articles:
        try:
            wf = wpdb.front.Fetcher(property_file_path, article, 'en')
            articles_xml.append(wf.xml)
        except:
            traceback.print_exc()
            print('Error encountered during fetching article! Quitting...')
            return False
        else:
            print(wf.url)
            print(wf.title)
            print(lxml.etree.tostring(wf.tree, pretty_print=True, encoding='UTF-8'))
            print('\n')

        articles_result = []
        for article_xml in articles_xml:
            cr = wpdb.middle.Cruncher(userstory3_crunches, article_xml)
            articles_result.append(cr.result)

        with open('out/out.csv', 'wb') as csv_file:
            import csv
            spamwriter = csv.writer(csv_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for result in articles_result:
                spamwriter.writerow(['name'] + result)

    return True

def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
