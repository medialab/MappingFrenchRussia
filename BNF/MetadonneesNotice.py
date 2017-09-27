import re

#class MetadonneesNotice
# Goal: Parse a BNF notice (from catalogue.bnf.fr)
# Usage: Give a BeautifulSoup tree (or similar tree) to parse method


class MetadonneesNotice():
	def __init__(self, ark_notice):
	# Data
		self.ark = ark_notice
		self.sep = ' // '
		self.csv_string_delim = '§'
		self.csv_field_delim = ','
		self.header_meta = ['Date', 'Langue']
		self.anchor_meta = ['DC.date', 'DC.language']
		#self.data_meta = ['', '']
		self.data_meta = []
		self.header_div = ['Notes', 'Résumé']
		self.anchor_div = ['note', 'resumeCnlj']
		#self.data_div = ['', '']
		self.data_div = []
		self.header_mixed = ['Éditeur', 'Description']
		self.anchor_mixed = [['DC.publisher', 'publication'], ['DC.format', 'descMat']]
		#self.data_mixed = ['', '']
		self.data_mixed = []
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
			if found is None:
				#self.data_meta[i] = self.header_meta[i] + ' absent.e'
				self.data_meta.append(self.header_meta[i] + ' absent.e')
			else:
				#self.data_meta[i] = found['content']
				self.data_meta.append(found['content'])

	def parse_div(self, soup):
		for i, item in enumerate(self.anchor_div):
			found = soup.find('div', attrs={'id':item})
			if found is None:
				#self.data_div[i] = self.header_div[i] + ' absent.e'
				self.data_div.append(self.header_div[i] + ' absent.e')
			else:
				span_list = found.find_all('span', attrs={'class':''})
				if span_list == []:
					#self.data_div[i] = self.header_div[i] + ' absent.e'
					self.data_div.append(self.header_div[i] + ' absent.e')
				else:
					for j in span_list:
						line = ""
						for k in j.stripped_strings:
							if 'Voir les notices' not in k:
								line+=k
						#self.data_div[i] += line#TODO: check that
						self.data_div.append(line)

	def parse_mixed(self, soup):
		for i, item in enumerate(self.anchor_mixed):
			found = soup.find('meta', attrs={'name':item[0]})
			if found is None:
				found = soup.find('div', attrs={'id':item[1]})
				if found is None:
					#self.data_mixed[i] = self.header_mixed[i] + ' absent.e'
					self.data_mixed.append(self.header_mixed[i] + ' absent.e')
				else:
					span_list = found.find_all('span', attrs={'class':''})
					if span_list == []:
						#self.data_mixed[i] = self.header_mixed[i] + ' absent.e'
						self.data_mixed.append(self.header_mixed[i] + ' absent.e')
					else:
						for j in span_list:
							line = ""
							for k in j.stripped_strings:
								if 'Voir les notices' not in k:
									line+=k
							#self.data_mixed[i] += line#TODO: check that
							self.data_mixed.append(line)
			else:
				#self.data_mixed[i] = found['content']
				self.data_mixed.append(found['content'])

	def parse_subjects(self, soup):
		found = soup.find('div', attrs={'id':'sujet'})
		if found is None:
			self.subjects.append('Sujets absent.e')
			self.subjects_links.append('Sujets absent.e')
		else:
			span_list = found.find_all('span', attrs={'class':''})
			if span_list == []:
				self.subjects.append('Sujets absent.e')
				self.subjects_links.append('Sujets absent.e')
			else:
				for j in span_list:
					line = ""
					for k in j.stripped_strings:
						if 'Voir les notices' not in k:
							line+=k
					self.subjects.append(line)#TODO: check that
					link = j.find('a', attrs={'class':'pictos'})
					if link is None:
						self.subjects_links.append('Pas de lien')
					else:
						self.subjects_links.append('http://catalogue.bnf.fr'+link['href'])
	def parse_title(self, soup):
		found = soup.find('meta', attrs={'name':'DC.title'})
		if found is None:
			found = soup.find('div', attrs={'id':'titre'})
			if found is None:
				self.title_raw = 'Titre absent'
				self.title_clean = 'Titre absent'
			else:
				span_list = found.find_all('span', attrs={'class':''})
				if span_list == []:
					self.title_raw = 'Titre absent'
				else:
					for j in span_list:
						line = ""
						for k in j.stripped_strings:
							if 'Voir les notices' not in k:
								line+=k
						self.title_raw += line#TODO: check that
		else:
			self.title_raw = found['content']
		if self.title_raw != 'Titre absent':
			tab = re.split('(.+?)(?=(?:\. )|(?: ?\/))', self.title_raw)
			self.title_clean = tab[1]

	def seek_role(self, span, default):
		line = ""
		for k in span.stripped_strings:
			if 'Voir les notices' not in k:
				line+=k
		tab = re.split('(.+?)(?=(?: \()|(?:\. ))(?: \(([0-9\.\?]{3,5}-[0-9\.\?]{3,5})?[ ;,]{0,3}(.*?)\))?(?:\. (.*))?', line)#(.+?)(?=(?: \()|(?:\. ))(?: \(([0-9\.\?]{3,5}-[0-9\.\?]{3,5})?[ ;,]{0,3}(.+?)\))?(?:\. (.*))? reste les roles
		birth = 'Pas de naissance'
		death = 'Pas de mort'
		role = default
		if len(tab) == 1:
			name = tab[0]
		else:
			name = tab[1] #ou approchant
			if tab[2] is not None:
				date = tab[2].split('-')
				birth = date[0]
				death = date[1]
			if tab[3] is not None:
				role += tab[3]
			if tab[4] is not None:
				role += tab[4]
		for i, item in enumerate(self.contributors):
			for j in item[0]:
				if name not in item[2] and j in role.lower():
					self.contributors_classified.add(name)
					item[2].append(name)
					item[3].append(birth)
					item[4].append(death)
					#Link searchin'
					link = span.find('a', attrs={'class':'pictos'})
					if link is None:
						item[5].append('Pas de lien')
					else:
						item[5].append('http://catalogue.bnf.fr'+link['href'])
		for i, item in enumerate(self.contributors[-1][2]):#== on garbage TODO: make it better ?
			if item in self.contributors_classified:#Classified elsewhere: remove from garbage
				self.contributors[-1][2].pop(i)
				self.contributors[-1][3].pop(i)
				self.contributors[-1][4].pop(i)
				self.contributors[-1][5].pop(i)

	def parse_contributors(self, soup):
		anchors = [['auteur', 'Auteur'],['autreAuteur', '']]
		for i in anchors:
			found = soup.find('div', attrs={'id':i[0]})
			if found is not None:
				span_list = found.find_all('span', attrs={'class':''})
				if span_list != []:
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

	def dump_schema(self):
		#Ark
		csv = 'Ark'
		#Contrib
		for i in self.contributors:
			csv += self.csv_field_delim+self.csv_string_delim+i[1]+self.csv_string_delim+self.csv_field_delim\
			+self.csv_string_delim+'Naissance '+i[1]+self.csv_string_delim+self.csv_field_delim\
			+self.csv_string_delim+'Mort '+i[1]+self.csv_string_delim+self.csv_field_delim\
			+self.csv_string_delim+'Lien '+i[1]+self.csv_string_delim
		#Subjects
		csv += self.csv_field_delim+'Sujets'+self.csv_field_delim+'Lien sujets'
		#Titles
		csv += self.csv_field_delim+'Titre nettoyé'+self.csv_field_delim+'Titre brut'
		#Mixed - Meta - Div
		for i in [self.header_mixed, self.header_meta, self.header_div]:
			for j in i:
				csv += self.csv_field_delim + j
		csv += '\n'
		return csv


	def to_csv(self):
		#Ark
		csv = self.ark
		#Contrib
		for i in self.contributors:
			for field in range(len(i)-2):
				csv += self.csv_field_delim
				if i[field+2] != []:
					csv += self.csv_string_delim
					csv += i[field+2][0]
					for j in range(len(i[field+2])-1):
						csv+=self.sep+i[field+2][j+1]
					csv += self.csv_string_delim
		#Subjects
		for i in [self.subjects, self.subjects_links]:
			csv += self.csv_field_delim
			if i != []:
				csv += self.csv_string_delim+i[0]
				for j in range(len(i)-1):
					csv += self.sep+i[j+1]
				csv += self.csv_string_delim
		#Titles
		csv += self.csv_field_delim+self.csv_string_delim+self.title_clean+self.csv_string_delim+self.csv_field_delim+self.csv_string_delim+self.title_raw+self.csv_string_delim
		#Mixed - Meta - Div
		for i in [self.data_mixed, self.data_meta, self.data_div]:
			for j in i:
				csv += self.csv_field_delim
				if j != '':
					csv += self.csv_string_delim + j + self.csv_string_delim
		csv+='\n'
		return csv
