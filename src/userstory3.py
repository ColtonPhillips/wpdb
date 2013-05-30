from pprint import pprint as pp

# This is a user story jam by Colton Phillips for Pascal Courty.
# The location is Colton's house
# Apr 10 2013

# A User story is a
QUEST = """I want to use your wpdb module to create a csv file filled with 8 explicit properties on a list
of articles. The output must be formatted in a csv file for use with Stata software. """

import wpdb
import traceback

def num_images(data):
    soup = data['soup']
    return str(len(soup.find('images')))

def daily_views_last_month(data):
    import urllib, re
    website = urllib.urlopen("http://stats.grok.se/en/latest30/" + str(data['title'])).read()
    pattern = r'(?<=viewed )\d*'
    prog = re.compile(pattern)
    match_object = prog.search(website)
    return str(match_object.group(0)) 
    
def byte_count(data):
    soup = data['soup']
    return str(soup.find('page')['length'])
 
def featured(data):
    soup = data['soup']
    for element in soup.find('categories'):
        if element['title'] == 'Category:Featured articles':
            return 'true'
    return 'false'
    
def good_article(data):
    soup = data['soup']
    for element in soup.find('categories'):
        if element['title'] == 'Category:Good articles':
            return 'true'
    return 'false'
    
def article_name(data):
    return data['title']

userstory3_crunches = [article_name, num_images, daily_views_last_month, byte_count, featured, good_article]
crunch_titles = ['Article','number of images', 'daily views last month', 'byte count','featured', 'good article']

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
            print wf.url
            print wf.title
            print wf.soup.prettify(encoding='UTF-8')
            print "\n"

        articles_result = []
        for article_xml in articles_xml:
            cr = wpdb.middle.Cruncher(userstory3_crunches, article_xml)
            articles_result.append(cr.result)

        with open('out/out.csv', 'wb') as csv_file:
            import csv
            spamwriter = csv.writer(csv_file, delimiter=',',
                            quotechar='"', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(crunch_titles)
            for result, article in zip(articles_result, articles):
                print result, article
                # Best way to relate the result to the article name? - CP
                spamwriter.writerow([article] + result)

    return True

def main():
    if (user_story() == False):
        print QUEST
    
if __name__ == "__main__":
    main()
