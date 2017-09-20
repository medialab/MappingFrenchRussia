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
		self.contributors_classified = set({})
		self.contributors = [ (('auteur',), 'Auteur', [], [], [], []),
		(('traducteur',), 'Traducteur', [], [], [], []),
		(('editeur scientifique', 'éditeur scientifique'), 'Éditeur scientifique', [], [], [], []),
		(('directeur de publication',), 'Directeur de publication', [], [], [], []),
		(('illustrateur', 'dessinateur', 'graphiste'), 'Illustrateur - Dessinateur - Graphiste', [], [], [], []),
		(('prefacier', 'postfacier'), 'Pre/PostFacier', [], [], [], []),
		(('collaborateur',), 'Collaborateur', [], [], [], []),
		(('redacteur', 'rédacteur'), 'Rédacteur', [], [], [], []),
		(('adaptateur',), 'Adaptateur', [], [], [], []),
		(('rôle indéterminé', 'fonction inconnue', ''), 'Rôle indéterminé', [], [], [], [])#TODO: make a better thing ?
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

	def seek_role(self, span, default):
		line = ""
		for k in span.stripped_strings:
			if ('Voir les notices' not in k):
				line+=k
		tab = re.split('(.+?)(?=(?: \()|(?:\. ))(?: \(([0-9\.\?]{3,5}-[0-9\.\?]{3,5})?[ ;,]{0,3}(.*?)\))?(?:\. (.*))?', line)#(.+?)(?=(?: \()|(?:\. ))(?: \(([0-9\.\?]{3,5}-[0-9\.\?]{3,5})?[ ;,]{0,3}(.+?)\))?(?:\. (.*))? reste les roles
		name = tab[1] #ou approchant
		birth = ''
		death = ''
		if (tab[2] is not None):
			date = tab[2].split('-')
			birth = date[0]
			death = date[1]
		role = default
		if (tab[3] is not None):
			role += tab[3]
		if (tab[4] is not None):
			role += tab[4]
		for i, item in enumerate(self.contributors):
			for j in item[0]:
				if (name not in item[2] and j in role.lower()):
					self.contributors_classified.add(name)
					item[2].append(name)
					item[3].append(birth)
					item[4].append(death)
					#Link searchin'
					link = span.find('a', attrs={'class':'pictos'})
					if (link is None):
						item[5].append('Pas de lien')
					else:
						item[5].append('http://catalogue.bnf.fr'+link['href'])
		for i, item in enumerate(self.contributors[-1][2]):#== on garbage TODO: make it better ?
			if (item in self.contributors_classified):#Classified elsewhere: remove from garbage
				self.contributors[-1][2].pop(i)
				self.contributors[-1][3].pop(i)
				self.contributors[-1][4].pop(i)
				self.contributors[-1][5].pop(i)

	def parse_contributors(self, soup):
		anchors = [['auteur', 'Auteur'],['autreAuteur', '']]
		for i in anchors:
			found = soup.find('div', attrs={'id':i[0]})
			if (found is not None):
				span_list = found.find_all('span', attrs={'class':''})
				if (span_list != []):
					for j in span_list:
						self.seek_role(j, i[1])

	def parse(self, soup):
		self.parse_meta(soup)
		self.parse_div(soup)
		self.parse_mixed(soup)
		self.parse_subjects(soup)
		self.parse_title(soup)
		self.parse_contributors(soup)

	def dump(self):
		print(self.title_clean, self.data_meta, self.data_div, self.data_mixed, self.subjects, self.subjects_links, self.title_raw, self.contributors)

#	def dump_schema(self, soup):

#	def to_csv(self, soup)
