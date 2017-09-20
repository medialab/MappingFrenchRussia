import re

class MetadonneesNotice():
	def __init__(self, ark_notice):
	# Data
		self.header_meta = []
		self.anchor_meta = []
		self.data_meta = []
		self.header_div = []
		self.anchor_div = []
		self.data_div = []
		self.header_mixed = []
		self.anchor_mixed = [[], []]
		self.data_mixed = []
		self.subjects = []
		self.subjects_links = []
		self.contributors_done = set({})
		self.contributors = [ (('auteur',), 'Auteur', [], [], [], []),
	#[...]
		]

	def parse_meta(self, soup):
		for i, item in enumerate(self.anchor_meta):
			found = soup.find('meta', attrs={'name':item})
			if (found is None):
				self.data_meta[i] = self.header_meta[i] + ' absent.e'
			else:
				self.data_meta[i] = found['content']

	def parse_div(self, soup):
		for i, item in enumerate(self.anchor_div):
			found = soup.find('div', attrs={'class':item})
			if (found is None):
				self.data_div[i] = self.header_div[i] + ' absent.e'
			else:
				span_list = soup.find_all('span', attrs={'class':''})
				if (find_all = []):
					self.data_div[i] = self.header_div[i] + ' absent.e'
				else:
					for j in span_list:
						line = ""
						for k in j.stripped_strings:
							if ('Voir les notices' not in k):
								line+=k
						data_div[i] += line#TODO: check that

	def parse(self, soup):
		parse_meta(soup)
		parse_div(soup)
		parse_mixed(soup)
		parse_subjects(soup)
		parse_contributors(soup)

#	def dump_schema(self, soup):

#	def to_csv(self, soup)
