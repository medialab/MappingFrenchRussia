#!/usr/bin/python3
import scrapy
from bs4 import BeautifulSoup
import sys
#sys.path.append('../../../')
from MetadonneesNotice import *

class CountObject():
        def __init__(self):
            self.num = 0

class PerseeSpider(scrapy.Spider):
    """Download & save to CSV valid Persee notices (we include too old notices though)."""

    name = "Persee"

    def start_requests(self):
        start_url = 'http://oai.persee.fr/oai?verb=ListSets'
        #max_pages = 8528
        #max_pages = 1
        #for i in range(max_pages):
        #    request = scrapy.Request(url=url_header+str(i+1), callback=self.parse_list)
            #request.meta['batch'] = i+1
        #    yield request
        request = scrapy.Request(url=start_url, callback=self.parse_sets)
        obj = CountObject()
        request.meta['num'] = obj
        yield request

    def parse_sets(self, response):
        url_header = 'http://oai.persee.fr/oai?verb=ListIdentifiers&metadataPrefix=oai_dc&set='
        soup = BeautifulSoup(response.body, "lxml-xml")
        set_list = soup.find_all('set')
        setSpec = set_list[0].find('setSpec').string
        request = scrapy.Request(url=url_header+setSpec, callback=self.parse_subsets)
        request.meta['num'] = response.meta['num']
        yield request
        for i in range(len(set_list)-1):
            setSpec = set_list[i+1].find('setSpec').string
            request = scrapy.Request(url=url_header+setSpec, callback=self.parse_notice_list)
            request.meta['num'] = response.meta['num']
            yield request

    def parse_subsets(self, response):
        url_header = 'http://oai.persee.fr/oai?verb=ListIdentifiers&metadataPrefix=oai_dc&set='
        resume_header = 'http://oai.persee.fr/oai?verb=ListIdentifiers&resumptionToken='
        soup = BeautifulSoup(response.body, "lxml-xml")
        subset_list = soup.find_all('header')
        for i in subset_list:
            subsetSpec = i.find_all('setSpec')[1].string
            request = scrapy.Request(url=url_header+subsetSpec, callback=self.parse_notice_list)
            request.meta['num'] = response.meta['num']
            yield request
        resume_tail = soup.find('resumptionToken').string
        if (resume_tail is not None):
            request = scrapy.Request(url=resume_header+resume_tail, callback=self.parse_subsets)
            request.meta['num'] = response.meta['num']
            yield request

    def parse_notice_list(self, response):
        url_header = 'http://oai.persee.fr/oai?verb=GetRecord&metadataPrefix=oai_dc&identifier='
        resume_header = 'http://oai.persee.fr/oai?verb=ListIdentifiers&resumptionToken='
        soup = BeautifulSoup(response.body, "lxml-xml")
        notice_list = soup.find_all('header')
        for i in notice_list:
            notice_id = i.find('identifier').string
            if (notice_id is not None):
                #print(notice_id)
                #f = open(
                notice = MetadonneesNotice()
                request = scrapy.Request(url=url_header+notice_id, callback=self.parse_notice_dc)
                request.meta['noticeObject'] = notice
                request.meta['noticeId'] = notice_id
                request.meta['num'] = response.meta['num']
                yield request
        resume_tail = soup.find('resumptionToken').string
        if (resume_tail is not None):
            request = scrapy.Request(url=resume_header+resume_tail, callback=self.parse_notice_list)
            request.meta['num'] = response.meta['num']
            yield request

    def parse_notice_dc(self, response):
        response.meta['num'].num += 1
        print(response.meta['num'].num)
        url_header = 'http://oai.persee.fr/oai?verb=GetRecord&metadataPrefix=mods&identifier='
        notice = response.meta['noticeObject']
        soup = BeautifulSoup(response.body, "lxml-xml")
        notice.get_id(soup)
        notice.parse_dc(soup)
        request = scrapy.Request(url=url_header+response.meta['noticeId'], callback=self.parse_notice_mods)
        request.meta['noticeObject'] = notice
        request.meta['noticeId'] = response.meta['noticeId']
        yield request

    def parse_notice_mods(self, response):
        url_header = 'http://oai.persee.fr/oai?verb=GetRecord&metadataPrefix=marc&identifier='
        notice = response.meta['noticeObject']
        soup = BeautifulSoup(response.body, "lxml-xml")
        notice.parse_mods(soup)
        #print(notice.data['title'])
        #if 'russie' in notice.data['title'].lower():
        #    print('Oui!')
        if notice.validate():
            request = scrapy.Request(url=url_header+response.meta['noticeId'], callback=self.parse_notice_marc)
            request.meta['noticeObject'] = notice
            request.meta['noticeId'] = response.meta['noticeId']
            yield request

    def parse_notice_marc(self, response):
        notice = response.meta['noticeObject']
        soup = BeautifulSoup(response.body, "lxml-xml")
        notice.parse_marc(soup)
    #    f = open('/tmp/scrap_persee.csv', 'a')
        with open('/tmp/scrap_persee.csv', 'a') as f:
            f.write(notice.to_csv())
    #    f.close()
