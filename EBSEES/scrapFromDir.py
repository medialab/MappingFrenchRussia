from bs4 import BeautifulSoup
#import requests
import os
import sys
from MetadonneesNotice import *

# /!\ This code IS **TAB INDENTED** /!\

# Get CSV from HTML notice directory

#html = requests.get('http://ebsees.staatsbibliothek-berlin.de/search.html?data=10000&title=Wieviel-Zeit-bleibt-Bosnien-noch-').text
#f = open('/home/sg/pageebsees.html')
#html = f.read()
#f.close()
#print(html)

def parse_dir():
    full_csv = ''
    arbre = os.walk(sys.argv[1])
    for subrep in arbre:
        for filename in subrep[2]:
            if filename.endswith('.html'):
                basename = filename.split('.')[0]
                print('\r'+basename, end='')
                #f = open(sys.argv[1]+filename, 'r')
                with open(sys.argv[1]+filename, 'r') as f:
                    html = f.read()
                #f.close()
                #print(html)
                soup = BeautifulSoup(html, 'lxml')
                notice = MetadonneesNotice()
                notice.parse(soup)
                #f = open(sys.argv[1]+basename+'.csv', 'w')
                #f.write(notice.to_csv())
                #f.close()
                if notice.valid():
                    full_csv += notice.to_csv()
        return full_csv

def debug_notice():
    #f = open('/home/sg/MFR/MappingFrenchRussia/EBSEES/scrap_data/extract-id1003.html')
    with open('/home/sg/MFR/MappingFrenchRussia/EBSEES/scrap_data/extract-id1003.html') as f:
        html = f.read()
    #f.close()
    soup = BeautifulSoup(html, 'lxml')
    notice = MetadonneesNotice()
    notice.parse(soup)
    notice.dump()
    print(notice.to_csv())

fc = parse_dir()
#f = open(sys.argv[2], 'w')
with open(sys.argv[2], 'w') as f:
    f.write(fc)
#f.close()
#debug_notice()

#csv = notice.dump_schema()+notice.to_csv()
#f = open('/home/sg/test.csv', 'w')
#f.write(csv)
#f.close()
#print("Written")
