#!/Python27/python
# -*- coding: UTF-8 -*-

import re

def write_file(filename, data):
    f = open(filename, 'w+')
    for item in data:
        f.write("%s\n" % item)
    f.close()

def main():
    f = open('Wps2', 'r')
    list = f.readlines()
    list = [_.rstrip('\n') for _ in list]
    f.close()
    newlist = []
    notfound = []

    for i in range(len(list)):
        name = re.match("^(?P<name>[\s\w^@\'\.\-\!\(\)]+)", list[i])
        if name:
            newlist.append(name.group('name'))       
        else:
            newlist.append(list[i])
    write_file('Wps2new', newlist)
    #write_file('remaining2.txt', notfound)    

if __name__ == "__main__":
    main()