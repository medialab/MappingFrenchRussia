class MetadonneesNotice():
	def __init__(self):
		#self.fields = {'ID':'', 'Title':'', 'Author(s)':'', 'Year':'', 'Pages':'',\
		#'Editor(s)':'', 'Published':'', 'Language(s)':'', 'Publsiher':'', 'Place':'',\
		#'ISBN':'', 'ISSN':'', 'Series':'', 'Subjects':[], 'Note':'', 'Medium':'', 'PURL':''}
		self.fields_header = ['ID', 'Title', 'Author(s)', 'Year', 'Pages',\
		'Editor(s)', 'Published', 'Language(s)', 'Publsiher', 'Place',\
		'ISBN', 'ISSN', 'Series', 'Subjects', 'Note', 'Medium', 'PURL']
		self.fields_data = ['', '', '', '', '', '', '', '', '', '', '', '', '', [], '', '', '']

	def parse(self, soup):
		table = soup.find('table', attrs={'class':'table table-bordered table-striped'})
		if (table is not None):
			tr_list = table.find_all('tr')
			for i in tr_list:
				line = ''
				if (i.td.string == "PURL"):
					line = 'http://ebsees.staatsbibliothek-berlin.de/'+i.td.next_sibling.a['href']
					self.fields_data[self.fields_header.index(i.td.string)] += line
				elif (i.td.string == "Subjects"):
					#self.fields['Subjects'] = []
					tag = i.td.next_sibling.a
					line = ''
					while(tag is not None):
						if (tag.name == u'a'):
							if (line != ''):
								line += ', '
							line += tag.string
						elif (tag.name == u'font'):
							self.fields_data[self.fields_header.index('Subjects')].append((line, 'http://ebsees.staatsbibliothek-berlin.de/search.html'+tag.a['href']))
							line = ''
						elif (tag.name == u'br' and line != ''):
							self.fields_data[self.fields_header.index('Subjects')].append((line, 'http://ebsees.staatsbibliothek-berlin.de/search.html'+tag.previous_sibling['href']))
							line = ''
						tag = tag.next_sibling
				else:
					self.fields_data[self.fields_header.index(i.td.string)] += i.td.next_sibling.string
	def dump(self):
		print(self.fields_data)

	def to_csv(self):
		csv = ''
		for value in self.fields_data:
			csv += '§'
			if (type(value) == list):
				csv += value[0][0] + ': ' + value[0][1]
				for i in range(len(value)-1):
					csv += ' // ' + value[i+1][0] + ': ' + value[i+1][1]
			else:
				csv += value
			csv += '§,'
		return csv[:-1]
			
		