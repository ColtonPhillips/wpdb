import MySQLdb
import sys

def main():
    import urllib
    xml = urllib.urlopen("http://stats.grok.se/en/latest30/A_Dangerous_Path")
    
    file = open ("out.txt", 'w')
    file.write(str(xml.read()))

if __name__ == "__main__":
    main()
