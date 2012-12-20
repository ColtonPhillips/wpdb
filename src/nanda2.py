import sys
import MySQLdb
import urllib
import re
import time
import profile

# what information should I be logging to the user? - CP

from xml.dom.minidom import parse
from datetime import date, timedelta

# TODO: Isn't the rv limit set by params passing to the program? Not hard coded? - CP
rvlimit = 400
rvend = '20121231'
rvstart = '20010101'

# TODO: Do this right, and test it works - CP
d = date(int(rvend[:4]), 12, 31)
ds = date(int(rvstart[:4]), 01, 01)
date1 = d

def main():
    
    # TODO: This really irks me. Putting in a class? - CP
    global date1
    global rvend
    global rvstart
    global ds
    global d
        
    #TODO: We don't really want to read a list we want to randomly gen. on the fly - CP
    #Read list
    if len(sys.argv) > 1:
        f = open(sys.argv[1], "r")
        list = f.readlines()
        list = [_.rstrip('\n') for _ in list]
        f.close()
    else:
        print "[*] missing list\n"
        exit(1)
    
    #Request and parse XML
    for title in list:
        print "[*] fetching page: %s\n" % (title)
        while date1 > ds:
            url = "http://en.wikipedia.org/w/api.php?action=query&format=xml&titles=%s&prop=info|revisions|categories&inprop=protection|url|readable|subjectid|watched&rvprop=userid|ids|timestamp|user|flags|comment|size&rvdir=older&rvstart=%s000000&rvend=%s000000&rvlimit=%d&clprop=timestamp" % (title, rvend, rvstart, rvlimit)
            print url
            xml = urllib.urlopen(url)
            parse_xml(xml)
            print "date is %s" % (date1)
            time.sleep(5)
            rvend = ''.join(str(date1).split('-'))
            
            file = open("temp.txt", "w")
            file.write(str(xml))
            file.close()

        date1 = d
        rvend = ''.join(str(d).split('-'))
    
    # TODO: Looks like talk pages must be done in seperate query. shit son. - CP
    
    #Request and parse XML for talk page
#    print "[*] time to talk baby!\n"
#    print "rv end is %s" % rvend
#    for title in list:
#        print "[*] fetching page: %s\n" % (title)
#        while date1 > ds:
#            url = "http://en.wikipedia.org/w/api.php?action=query&format=xml&titles=Talk:%s&prop=info|revisions&inprop=protection|url|readable|subjectid|watched&rvprop=userid|ids|timestamp|user|flags|comment|size|content&rvdir=older&rvstart=%s000000&rvend=%s000000&rvlimit=%d&clprop=timestamp" % (title, rvend, rvstart, rvlimit)
#            print url
#            xml = urllib.urlopen(url)
#            parse_xml(xml, True)
#            print "date is %s" % (date1)
#            time.sleep(5)
#            rvend = ''.join(str(date1).split('-'))
#        date1 = d
#        rvend = ''.join(str(d).split('-'))
    
    print "[*] all done, now roll me a joint!"
        
def parse_xml(xml, talk=False):
    
    global date1, d, ds, rvend
    
    pxml = parse(xml)
    page = pxml.getElementsByTagName('page')[0]
    protection = pxml.getElementsByTagName('pr')
    revisions = pxml.getElementsByTagName('rev')
    categories = pxml.getElementsByTagName('cl')
    attributes = {}
    
    if len(revisions) == 0:
        print "[*] page does not exist or it had no revisions within the time span you asked for!\n"
        date1 = ds - timedelta(days=1)
        return 0
    
    #TODO: This could be made more clear and consise whats going on here probably... - CP
    for attribute in page.attributes.keys():
        attributes[attribute] = page.attributes[attribute].value.encode('ascii', 'ignore')\
				.replace("\\", "\\\\").replace("'", "\\'")
    title = attributes['title']
    
    if date1 == d:
        sql(attributes, 'pages')        
        for element in protection:
            for attribute in element.attributes.keys():
                attributes[attribute] = element.attributes[attribute].value.encode('ascii', 'ignore')\
                                        .replace("\\", "\\\\").replace("'", "\\'")
            sql(attributes, 'protection')
    
    for element in revisions:
        for attribute in element.attributes.keys():
            attributes[attribute] = element.attributes[attribute].value.encode('ascii', 'ignore')\
                                    .replace("\\", "\\\\").replace("'", "\\'")
        timestamp = attributes['timestamp'].split('T') # 2005-06-01T20:10:56Z becomes ['2012-02-29', '08:50:45Z']
        attributes['date'] = timestamp[0] # 2012-02-29
        attributes['time'] = timestamp[1][:-1] # 08:50:45
        date1 = timestamp[0].split('-')
        date1 = date(int(date1[0]),int(date1[1]),int(date1[2]))
        if date1 != ds:
             date1 = date1 - timedelta(days=1)
        print attributes['date'], date1

        if date1 < ds:
            print "date too big, returning"
            return 0
        
        #Validate1 Attributes
        if 'redirect' in attributes:
            print "[*] page redirect (ignoring %s)\n" % (title)
            return 0
        
        if 'minor' in attributes:
            attributes['minor'] = '1'
        else:
            attributes['minor'] = '0'
        
        if 'parentid' not in attributes:
            print "[*] reached first revision!\n"
            attributes["parentid"] = -1
        
        attributes['data'] = ''
        sql(attributes, 'revisions')
        
        if element.firstChild:
            data = element.firstChild.data.encode('ascii', 'ignore')
            data = data.replace('\'', '\\\'')
            attributes['data'] = data
    
        if talk is True:
            parse_talk(**attributes)
    
    if talk is False:
         for element in categories:
            for attribute in element.attributes.keys():
                attributes[attribute] = element.attributes[attribute].value.encode('ascii', 'ignore')\
                                        .replace("\\", "\\\\").replace("'", "\\'")
            timestamp = attributes['timestamp'].split('T') # 2005-06-01T20:10:56Z becomes ['2012-02-29', '08:50:45Z']
            attributes['date1'] = timestamp[0] # 2012-02-29
            attributes['time'] = timestamp[1][:-1] # 08:50:45
            attributes['category'] = attributes['title'][9:]
            attributes['title'] = title
            sql(attributes, 'categories')
        
def parse_talk(**attributes):
    data = attributes['data']
    # talk_title = re.compile("==(?P<title>[^==]+)==")
    talk_wikip = re.compile("{{(?P<name>\w+(\s\w+)*)\|(?P<qap>(class|importance)=(?P<r>\w*))(\|(?P<qap1>(class|importance)=(?P<r1>\w*)))?")
    #{{(?P<name>(\s?\w+)*)(\|[A-z\-\&]*=\w*)?\|(?P<qap>(class|importance)=(?P<r>\w*))(\|[A-z\-\&]*=\w*)?(\|(?P<qap1>(class|importance)=(?P<r1>\w*)))?
    projects = [_.groupdict() for _ in talk_wikip.finditer(data)]
    #projects = []
    #    for i in talk_wikip.finditer(data):
    #        projects.append(i.groupdict())
    #print projects
    # headers = ""
    # headers_r = talk_title.findall(data)
    # headers_r = [_.strip() for _ in headers_r]
    # headers = ', '.join(headers_r,)
    # count = len(headers_r)
    
    def parse_wikiproject(wikip):
        if wikip['qap'][1] == 'c':
            attributes['quality'] = wikip['r1'] #add check to see if they exist
            attributes['priority'] = wikip['r']    
        else:
            attributes['quality'] = wikip['r']
            attributes['priority'] = wikip['r1']       
       
        attributes['wikiproject'] = wikip['name']
        sql(attributes, 'projects')
        
    # attributes['headers'] = headers
    # attributes['header_count'] = count
    attributes['data'] = ''
    # sql(attributes, 'talk')
        
    if not projects:
        print "[*] no wikiprojects\n"
    else:
        for project in projects:
            parse_wikiproject(project)
    
# TODO: Sanitize SQL entries - CP
# TODO: 
def sql(values, type):
    
    #SQL Ju-Ju
    try:
        conn = MySQLdb.connect(
                    host = "127.0.0.1",
                    user = "root",
                    passwd = "dangermouse",
                    db = "wpdb")
    except MySQLdb.Error, e:
        print("%s") % e
        exit(1)
        
    def execute(sql):
        cursor = conn.cursor()
        try:
            cursor.execute(sql)
            conn.commit()
            #print("Inserted to MySQL Database successfully!\n")
        except MySQLdb.Error, e:
            conn.rollback()
            print("FAILED: %s\n") % e
        
        cursor.close()
        
    #Populate `wiki`.`pages` table
    if type == 'pages':
        query = "INSERT INTO `wiki`.`pages` (\
        `lastrevid`, \
        `pageid`, \
        `title`, \
        `editurl`, \
        `counter`, \
        `readable`, \
        `length`, \
        `touched`, \
        `ns`, \
        `fullurl` \
        ) VALUES (%i, %i, '%s', '%s', '%s', '%s', %i, '%s', %i, '%s')" % (int(values['lastrevid']), int(values['pageid']), values['title'], values['editurl'],\
                                                                                values['counter'], values['readable'], int(values['length']),\
                                                                                values['touched'], int(values['ns']), values['fullurl'])
        
        #print("\nSQL Query: %s\n") % query
        execute(query)

    #Populate `wiki`.`page_revisions` table
    if type == 'revisions':
        query = "INSERT INTO `wiki`.`page_revisions` ( \
        `title`, \
        `comment`, \
        `date`, \
        `time`, \
        `userid`, \
        `revid`, \
        `user`, \
        `parentid`, \
        `minor`, \
        `size`, \
        `data` \
        ) VALUES ('%s', '%s', '%s', '%s', %i, %i, '%s', %i, '%s', %i, '%s')" % (values['title'], values['comment'], values['date'], values['time'],\
                                                                                int(values['userid']), int(values['revid']), values['user'], int(values['parentid']),\
                                                                                values['minor'], int(values['size']), values['data'])
        
        #print("\nSQL Query: %s\n") % query
        execute(query)

    #Populate `wiki`.`talk_revisions` table
   #  if type == 'talk':
    #     query = "INSERT INTO `wiki`.`talk_revisions` ( \
     #    `revid`, \
     #    `headers`, \
     #    `header_count` \
      #   ) VALUES (%i, '%s', %i)" % (int(values['revid']), values['headers'], int(values['header_count']))
        
        #print("\nSQL Query: %s\n") % query
     #    execute(query)
 
    #Populate `wiki`.`talk_projects` table       
    if type == 'projects':
        query = "INSERT INTO `wiki`.`talk_projects` ( \
        `date`,\
        `time`,\
        `revid`, \
        `name`, \
        `quality`, \
        `priority` \
        ) VALUES ('%s', '%s', %i, '%s', '%s', '%s')" % (values['date'], values['time'], int(values['revid']), values['wikiproject'], values['quality'], values['priority'])
        
        #print("\nSQL Query: %s\n") % query
        execute(query)
        
    #Populate `wiki`.`page_categories` table       
    if type == 'categories':
        query = "INSERT INTO `wiki`.`page_categories` ( \
        `date`, \
        `time`, \
        `title`, \
        `category` \
        ) VALUES ('%s', '%s', '%s', '%s')" % (values['date'], values['time'], values['title'], values['category'])
        
        #print("\nSQL Query: %s\n") % query
        execute(query)
        
    #Populate `wiki`.`page_protection` table       
    if type == 'protection':
        query = "INSERT INTO `wiki`.`page_protection` ( \
        `title`, \
        `type`, \
        `level`, \
        `expiry` \
        ) VALUES ('%s', '%s', '%s', '%s')" % (values['title'], values['type'], values['level'], values['expiry'])
        
        #print("\nSQL Query: %s\n") % query
        execute(query)
        
    #Close MySQL connection
    conn.close()

if __name__ == "__main__":
    #profile.run('main()')
    main()