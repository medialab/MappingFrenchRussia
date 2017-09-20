import re

class MetadonneesNotice():
	def __init__(self, ark_notice):
	# Data
		self.ark = ark_notice
		self.sep = ' // '
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

	def parse_mixed(self, soup):
		for i, item in enumerate(self.anchor_mixed):
			found = soup.find('meta', attrs={'name':item[0]})
			if (found is None):
				found = soup.find('div', attrs={'id':item[1]})
				if (found is None):
					self.data_mixed[i] = self.header_mixed[i] + ' absent.e'
				else:
					span_list = found.find_all('span', attrs={'class':''})
					if (span_list == []):
						self.data_mixed[i] = self.header_mixed[i] + ' absent.e'
					else:
						for j in span_list:
							line = ""
							for k in j.stripped_strings:
								if ('Voir les notices' not in k):
									line+=k
							self.data_mixed[i] += line#TODO: check that
			else:
				self.data_mixed[i] = found['content']

	def parse_subjects(self, soup):
		found = soup.find('div', attrs={'id':'sujet'})
		if (found is None):
			self.subjects.append('Sujets absent.e')
			self.subjects_links.append('Sujets absent.e')
		else:
			span_list = found.find_all('span', attrs={'class':''})
			if (span_list == []):
				self.subjects.append('Sujets absent.e')
				self.subjects_links.append('Sujets absent.e')
			else:
				for j in span_list:
					line = ""
					for k in j.stripped_strings:
						if ('Voir les notices' not in k):
							line+=k
					self.subjects.append(line)#TODO: check that
					link = j.find('a', attrs={'class':'pictos'})
					if (link is None):
						self.subjects_links.append('Pas de lien')
					else:
						self.subjects_links.append('http://catalogue.bnf.fr'+link['href'])
	def parse_title(self, soup):
		found = soup.find('meta', attrs={'name':'DC.title'})
		if (found is None):
			found = soup.find('div', attrs={'id':'titre'})
			if (found is None):
				self.title_raw = 'Titre absent'
				self.title_clean = 'Titre absent'
			else:
				span_list = found.find_all('span', attrs={'class':''})
				if (span_list == []):
					self.title_raw = 'Titre absent'
				else:
					for j in span_list:
						line = ""
						for k in j.stripped_strings:
							if ('Voir les notices' not in k):
								line+=k
						self.title_raw += line#TODO: check that
		else:
			self.title_raw = found['content']
		if (self.title_raw != 'Titre absent'):
			tab = re.split('(.+?)(?=(?:\. )|(?: ?\/))', self.title_raw)
			self.title_clean = tab[1]

	def parse(self, soup):
		self.parse_meta(soup)
		self.parse_div(soup)
		self.parse_mixed(soup)
		self.parse_subjects(soup)
		self.parse_title(soup)
		#parse_contributors(soup)

	def dump(self):
		print(self.title_clean, self.data_meta, self.data_div, self.data_mixed, self.subjects, self.subjects_links, self.title_raw)

#	def dump_schema(self, soup):

#	def to_csv(self, soup)
