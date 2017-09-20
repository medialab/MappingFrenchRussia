import re

class MetadonneesNotice():
	def __init__(self, ark_notice):
	# Data
		self.ark = ark_notice
		self.header_meta = ['Date', 'Langue']
		self.anchor_meta = ['DC.date', 'DC.language']
		self.data_meta = ['', '']
		self.header_div = ['Notes', 'Résumé']
		self.anchor_div = ['note', 'resumeCnlj']
		self.data_div = ['', '']
		self.header_mixed = ['Éditeur', 'Description']
		self.anchor_mixed = [['DC.publisher', 'publication'], ['DC.format', 'descMat']]
		self.data_mixed = ['', '']
		self.title_clean = ""
		self.title_raw = ""
		self.subjects = []
		self.subjects_links = []
		self.contributors_done = set({})
		self.contributors = [ (('auteur',), 'Auteur', [], [], [], []),
		(('traducteur',), 'Traducteur', [], [], [], []),
		(('editeur scientifique', 'éditeur scientifique'), 'Éditeur scientifique', [], [], [], []),
		(('directeur de publication',), 'Directeur de publication', [], [], [], []),
		(('illustrateur', 'dessinateur', 'graphiste'), 'Illustrateur - Dessinateur - Graphiste', [], [], [], []),
		(('prefacier', 'postfacier'), 'Pre/PostFacier', [], [], [], []),
		(('collaborateur',), 'Collaborateur', [], [], [], []),
		(('redacteur', 'rédacteur'), 'Rédacteur', [], [], [], []),
		(('adaptateur',), 'Adaptateur', [], [], [], []),
		(('rôle indéterminé', 'fonction inconnue'), 'Rôle indéterminé', [], [], [], [])
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
			found = soup.find('div', attrs={'id':item})
			if (found is None):
				self.data_div[i] = self.header_div[i] + ' absent.e'
			else:
				span_list = found.find_all('span', attrs={'class':''})
				if (span_list == []):
					self.data_div[i] = self.header_div[i] + ' absent.e'
				else:
					for j in span_list:
						line = ""
						for k in j.stripped_strings:
							if ('Voir les notices' not in k):
								line+=k
						self.data_div[i] += line#TODO: check that

	def parse(self, soup):
		self.parse_meta(soup)
		self.parse_div(soup)
		#parse_mixed(soup)
		#parse_subjects(soup)
		#parse_contributors(soup)

	def dump(self):
		print(self.data_meta, self.data_div)

#	def dump_schema(self, soup):

#	def to_csv(self, soup)
