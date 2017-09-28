#!/usr/bin/python3
import scrapy
from bs4 import BeautifulSoup

#277 avec la zone

class CountObject():
		def __init__(self):
			self.num = 0

class SRUBNFSpider(scrapy.Spider):
	name = "SRUBNF"
	
	def start_requests(self):
		url_header = 'http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.ark=%22'
		url_footer = '%22&recordSchema=intermarcXchange'
		obj = CountObject()
		f = open('liste_ark_8000.csv', 'r')
		for line in f:
			#print(line[:-1])
			request = scrapy.Request(url=url_header+line[:-1]+url_footer, callback=self.parse_xml)
			request.meta['num'] = obj
			request.meta['ark'] = line
			yield request

	def parse_xml(self, response):
		soup = BeautifulSoup(response.body, "lxml-xml")
		zone250 = soup.find('datafield', attrs={'tag':'250'})
		#print(soup)
		if zone250 is not None:
			#print('There is !')
			if zone250.find('subfield', attrs={'code':'u'}) is not None:
				f = open('/tmp/ark_good', 'a')
				f.write(response.meta['ark'])
				f.close()
				response.meta['num'].num += 1
				print(response.meta['num'].num)
			else:
				f = open('/tmp/ark_noU', 'a')
				f.write(response.meta['ark'])
				f.close()
		else:
			f = open('/tmp/ark_no250', 'a')
			f.write(response.meta['ark'])
			f.close()