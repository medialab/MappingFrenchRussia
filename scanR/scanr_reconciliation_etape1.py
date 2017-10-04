import sys
import csv
import re
if len(sys.argv) < 3:
	print('Usage: '+sys.argv[0]+' [source] [destination]')
	sys.exit()

with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
	prefix = 'scanR_'
	normalized_columns = ('StdAuteur', 'StdTitre', 'StdSource', 'StdAnnée', 'StdMots-clés')
#f = open(sys.argv[1], 'r')
#g = open(sys.argv[2], 'w')
#h = open(sys.argv[3], 'w')
	sourceCSV = csv.reader(f, delimiter=';', quotechar='"')
	destCSV = csv.writer(g, delimiter=',', quotechar='"')
	#regex = re.compile('(?:.*?)(?:\\W|^)(?:(?:russ(?:i)?e)|(?:sovi[eé]t)|(?:urss(?!a)))(?:.*?)', flags=re.I)
# NOTE : column numbers ARE HARDCODED
#Authors: offset 6,5
#Title: offset 0
#Source: 11+8+9
#Year: offset 10 (filtering needed)
#Keywords: 17
	for i, line in enumerate(sourceCSV):
		#print(i)
		if not i:
			#destCSV.writerow(line)
			for j in range(len(line)):
				line[j] = prefix+line[j]
			for j in normalized_columns:
				line.append(prefix+j)
			destCSV.writerow(line)
		else:
			givenName_list = line[5].split(';')
			#print(givenName_list)
			familyName_list = line[6].split(';')
			authors = familyName_list[0]
			if givenName_list != ['']:
				authors += ', '+givenName_list[0]
			for j in range(len(familyName_list)-1):
				authors += ' // ' + familyName_list[j+1]
				if givenName_list != ['']:
					authors += ', '+givenName_list[j+1]
			line.append(authors)
			line.append(line[0])
			desc_bonus = ''
			if line[8] != '':
				desc_bonus += ' n° ' + line[8]
			if line[9] != '':
				desc_bonus += ' p ' + line[9]
			line.append(line[11]+desc_bonus)
			line.append(line[10].split('-')[0])
			line.append(line[17].replace(';', ' // '))
			destCSV.writerow(line)
#f.close()
#g.close()
#h.close()
print("Done")
