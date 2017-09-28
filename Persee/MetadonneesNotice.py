import re

#class MetadonneesNotice
# Goal: Parse a Persee notice
# Usage: Give a BeautifulSoup tree (or similar tree) to parse method

class MetadonneesNotice():
	def __init__(self):
		#self.valid_anchor = ('russie', 'russe', 'soviét', 'soviet', 'urss', 'u.r.s.s')
		self.dc_anchor = ('title', 'publisher', 'date', 'language')
		#self.mods_anchor = ('abstract') # + mods:name(given, family,+ role)
		self.marc_anchor = (('description', '787', 'gt'),) # marc (tag 787 / code g&t)
		self.data = {}

	def get_id(self, soup):
		self.data['id'] = soup.find('identifier').string
		
	def parse_dc(self, soup):
		for i in self.dc_anchor:
			tags = soup.find_all(i)
			if len(tags) > 1:
				self.data[i] = []
				for j in tags:
					self.data[i].append(j.string)
			elif len(tags) == 1:
				self.data[i] = tags[0].string
		
	def parse_mods(self, soup):
		self.data['names'] = []
		names = soup.find_all('name')
		for i in names:
			givenName = ''
			familyName = ''
			role = []
			identity = i.find_all('namePart')
			for j in identity:
				if j['type'] == "given":
					givenName = j.string
				elif j['type'] == "family":
					familyName = j.string
			roles = i.find_all('role')
			for j in roles:
				role.append(j.find('roleTerm').string)
			self.data['names'].append((givenName, familyName, role))
		abst = soup.find('abstract')
		if abst is not None and abst.string is not None:
			self.data['abstract'] = abst.string
			
	def parse_marc(self, soup):
		for i in self.marc_anchor:
			field = soup.find('datafield', attrs={'tag':i[1]})
			line = ''
			for j in i[2]:
				line += field.find('subfield', attrs={'code':j}).string+', '
			self.data[i[0]] = line[:-2]

	def validate(self):#TODO: test that !
		regex = re.compile('(?:^|\\W)(?:(?:russ(?:i)?e)|(?:sovi[eé]t)|(?:urss(?!a)))', flags=re.I)
		test = False
		if 'title' not in self.data and 'abstract' not in self.data:#Safety measure, you shouldn't do that anyway
			return False
		#for i in self.valid_anchor:
		#	if i in self.data['title'].lower() or ('abstract' in self.data and i in self.data['abstract'].lower()):
		if regex.match(self.data['title']) is not None or ('abstract' in self.data and regex.match(self.data['abstract']) is not None)
				test = True
		return test

	def dump(self):
		print(self.data)

	def to_csv(self):
		csv = self.data['id'] + ','
		if self.data['names'] != []:
			csv += '"' + self.data['names'][0][1].replace('"', '""') + '. ' + self.data['names'][0][0].replace('"', '""')
			for j in self.data['names'][0][2]:
				csv += '-'+ j
			for i in range(len(self.data['names'])-1):
				csv += ' // ' + self.data['names'][i+1][1].replace('"', '""') + '. ' + self.data['names'][i+1][0].replace('"', '""')
				for j in self.data['names'][i+1][2]:
					csv += '-' + j.replace('"', '""')
			csv += '"'
		for i in self.dc_anchor:
			csv += ','
			if type(self.data[i]) == list:
				if i != []:
					csv += '"' + self.data[i][0].replace('"', '""')
					for j in range(len(self.data[i])-1):
						csv += ' // ' + self.data[i][j+1].replace('"', '""')
					csv += '"'
			else:
				csv += '"' + self.data[i].replace('"', '""') + '"'
		for i in self.marc_anchor:
			csv += ',"'+self.data[i[0]].replace('"', '""')+'"'
		csv += ','
		if 'abstract' in self.data:
			csv += '"'+self.data['abstract'].replace('"', '""')+'"'
		return csv + '\n'
				