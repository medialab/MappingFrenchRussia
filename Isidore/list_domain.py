from bs4 import BeautifulSoup
import requests
import sys

# /!\ This code is **TAB INDENTED** /!\

# Get the source domain list (and occurence number) of notice list.

#from MetadonneesNotice import *

#html = requests.get('')
url_set = set({})
f = open(sys.argv[1])
for line in f:
	rep = requests.get(line[:-1])
	domain = rep.url.split('//')[1].split('/')[0]
	if domain not in url_set:
		print(domain)
		url_set.add(domain)
f.close()
print(url_set)