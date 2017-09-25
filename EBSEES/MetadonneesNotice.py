#coding=utf-8
class MetadonneesNotice():
	def __init__(self):
		#self.fields = {'ID':'', 'Title':'', 'Author(s)':'', 'Year':'', 'Pages':'',\
		#'Editor(s)':'', 'Published':'', 'Language(s)':'', 'Publsiher':'', 'Place':'',\
		#'ISBN':'', 'ISSN':'', 'Series':'', 'Subjects':[], 'Note':'', 'Medium':'', 'PURL':''}

		self.fields_header = ('ID', 'Title', 'Author(s)', 'Year', 'Pages',\
		'Editor(s)', 'Published', 'Language(s)', 'Publsiher', 'Place',\
		'ISBN', 'ISSN', 'Series', 'Subjects', 'Note', 'Medium', 'PURL')

		self.fields_data = {'ID': (1, []), 'Title': (1, []), 'Author(s)': (3, []), 'Year': (1, []), 'Pages': (1, []),\
		'Editor(s)': (3, []), 'Published': (3, []), 'Language(s)': (1, []), 'Publsiher': (3, []), 'Place': (1, []),\
		'ISBN': (1, []), 'ISSN': (1, []), 'Series': (1, []), 'Subjects': (3, []), 'Note': (1, []), 'Medium': (1, []), 'PURL': (2, [])}

		#self.fields_data = ([], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [])
		#self.fields_data = []
		#self.fields_flags = (1, 1, 3, 1, 1, 3, 3, 1, 3, 1, 1, 1, 1, 3, 1, 1, 2) # 1 for label only, 2 for link only, 3 for both

	def parse(self, soup):
		table = soup.find('table', attrs={'class':'table table-bordered table-striped'})
		if table is not None:
			tr_list = table.find_all('tr')
			for i in tr_list:
				#print(i.td.string)
				if (i.td.string == "Subjects"):
					#self.fields['Subjects'] = []
					tag = i.td.next_sibling.a
					line = ''
					while tag is not None:
						if tag.name == u'a' and tag.string is not None:
							if line != '':
								line += ', '
							line += tag.string
						elif tag.name == u'font':
				#			print(line)
							#self.fields_data[self.fields_header.index(i.td.string)].append((line, 'http://ebsees.staatsbibliothek-berlin.de/search.html'+tag.a['href']))
							self.fields_data[i.td.string][1].append((line, 'http://ebsees.staatsbibliothek-berlin.de/search.html'+tag.a['href']))
							line = ''
						elif tag.name == u'br' and line != '':
				#			print(line)
							#self.fields_data[self.fields_header.index(i.td.string)].append((line, 'http://ebsees.staatsbibliothek-berlin.de/search.html'+tag.previous_sibling['href']))
							self.fields_data[i.td.string][1].append((line, 'http://ebsees.staatsbibliothek-berlin.de/search.html'+tag.previous_sibling['href']))
							line = ''
						tag = tag.next_sibling
					#print(self.fields_data[self.fields_header.index('Subjects')])
				elif i.td.string in self.fields_header:
					link = 'Pas de lien'
					text = ''
					tag = i.td.next_sibling
					if tag.a is not None:
						link = 'http://ebsees.staatsbibliothek-berlin.de/search.html'+tag.a['href']
						text = tag.a.string
						if len(tag.contents) > 1:
							text += tag.contents[1]
					elif tag.string is None:#No links, but probably formatting (<br/> or other)
						for t in tag.stripped_strings:
							text += t
					else:
						text = tag.string
					#self.fields_data[self.fields_header.index(i.td.string)].append((text, link))
					self.fields_data[i.td.string][1].append((text, link))

	def dump(self):
		print(self.fields_data)

	def to_csv(self):
		csv = ''
		#for i, value in enumerate(self.fields_data):
		for field in self.fields_header:
			print(field)
			#print(i, value)
			#if value != []:
			if self.fields_data[field][1] != []:
				csv += '§'
				#if self.fields_flags[i]&1:
				if self.fields_data[field][0] & 1:
					#csv += value[0][0]
					#for j in range(len(value)-1):
					#	csv += ' // ' + value[j+1][0]
					csv += self.fields_data[field][1][0][0]
					for j in range(len(self.fields_data[field][1])-1):
						csv += ' // ' + self.fields_data[field][1][j+1][0]
					csv += '§,'
				#if self.fields_flags[i]&2:
				if self.fields_data[field][0] & 2:
					#csv += value[0][1]
					#for j in range(len(value)-1):
					#	csv += ' // ' + value[j+1][1]
					csv += self.fields_data[field][1][0][1]
					for j in range(len(self.fields_data[field][1])-1):
						csv += ' // ' + self.fields_data[field][1][j+1][1]
					csv += '§,'
			else:
				csv += ','
		return csv[:-1]+'\n'
			
		