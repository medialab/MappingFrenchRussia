#!/usr/bin/python3
import scrapy
from bs4 import BeautifulSoup

# /!\ This code is **TAB INDENTED** /!\

class CountObject():
		def __init__(self):
			self.num = {}

class IsidoreDomainSpider(scrapy.Spider):
	"""Get the source domain list (and occurence number) of notice list."""

	name = "IsidoreDomain"
	
	def start_requests(self):
		#url_header = 'http://catalogue.bnf.fr/api/SRU?version=1.2&operation=searchRetrieve&query=bib.ark=%22'
		#url_footer = '%22&recordSchema=intermarcXchange'
		obj = CountObject()
		f = open('liste_source_current', 'r')
		for line in f:
			#print(line[:-1])
			request = scrapy.Request(url=line[:-1], callback=self.parse_rep)
			request.meta['num'] = obj
			#request.meta['ark'] = line
			yield request

	def parse_rep(self, response):
		domain = response.url.split('//')[1].split('/')[0]
		url_dic = response.meta['num']
		if domain not in url_dic.num:
#			print(domain)
			url_dic.num[domain] = 1
		else:
			url_dic.num[domain] += 1
		nb = 0
		g = open('/tmp/list_domain', 'w')
		for key, item in url_dic.num.items():
			g.write(key)
			g.write(',')
			g.write(str(item))
			g.write('\n')
			nb += item
		g.close()
		print('\r', nb, end='')
		#print('\r', end='')
		#print(url_dic.num, end='')