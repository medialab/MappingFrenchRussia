#!/usr/bin/python3
import scrapy
from bs4 import BeautifulSoup
import sys

# /!\ This code is **TAB INDENTED** /!\

#sys.path.append('../../../')
#from MetadonneesNotice import *

class EBSEESSpider(scrapy.Spider):
    """Download all notices to directory."""

    name = "EBSEES"

    def start_requests(self):
        url_header = 'http://ebsees.staatsbibliothek-berlin.de/search.html?pageNum='
        max_pages = 8528
        #max_pages = 1
        for i in range(max_pages):
            request = scrapy.Request(url=url_header+str(i+1), callback=self.parse_list)
            #request.meta['batch'] = i+1
            yield request

    def parse_list(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        tr_list = soup.find('table', attrs={'class':'table table-bordered table-striped'}).find_all('tr')
        for i in tr_list:
            yield scrapy.Request(url=response.url.split('?')[0]+i.td.next_sibling.a['href'], callback=self.parse_notice)
    
    def parse_notice(self, response):
        #notice = MetadonneesNotice()
        #notice.parse(BeautifulSoup(response.body, "lxml"))
        #csv = notice.to_csv()
        #f = open('/home/sg/MFR/MappingFrenchRussia/EBSEES/scrap_data/extract-id'+response.meta['id'], 'w')
        #f = open('/home/sg/MFR/MappingFrenchRussia/EBSEES/scrap_data/extract-id'+notice.fields_data[0]+'.csv', 'w')
        #f.write(csv)
        #f.close()
        f = open('/home/sg/MFR/MappingFrenchRussia/EBSEES/scrap_data/extract-id'+response.url.split('?')[1].split('&')[0].split('=')[1]+'.html', 'wb')
        f.write(response.body)
        f.close()