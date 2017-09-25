class MetadonneesNotice():
	def __init__(self):
		self.dc_anchor = ('title', 'publisher', 'date', 'language')
		#self.mods_anchor = ('abstract') # + mods:name(given, family,+ role)
		self.marc_anchor = (('description', '787', 'gt'),) # marc (tag 787 / code g&t)
		self.data = {}

	def get_id(self, soup):
		data['id'] = soup.find('identifier').string
		
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
			
	def parse_marc(self, soup):
		for i in self.marc_anchor:
			field = soup.find('datafield', attrs={'tag':i[1]})
			line = ''
			for j in i[2]:
				line += field.find('subfield', attrs={'code':j}).string+', '
			self.data[i[0]] = line[:-2]

	def dump(self):
		print(self.data)
				