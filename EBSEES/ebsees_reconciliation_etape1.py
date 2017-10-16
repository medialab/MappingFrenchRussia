import sys
import csv
import re

# /!\ This code IS **TAB INDENTED** /!\

# TODO: make this a clean importable module

# Goal: Add standard (standard as "common for all the datasets") fields with proper formatting

if len(sys.argv) < 3:
	print('Usage: '+sys.argv[0]+' [source] [destination]')
	sys.exit()

with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
	prefix = 'EBSEES_'
	normalized_columns = ('StdAuteur', 'StdTitre', 'StdSource', 'StdAnnée', 'StdMots-clés')
#f = open(sys.argv[1], 'r')
#g = open(sys.argv[2], 'w')
#h = open(sys.argv[3], 'w')
	sourceCSV = csv.reader(f, delimiter=',', quotechar='"')
	destCSV = csv.writer(g, delimiter=',', quotechar='"')
	#regex = re.compile('(?:.*?)(?:\\W|^)(?:(?:russ(?:i)?e)|(?:sovi[eé]t)|(?:urss(?!a)))(?:.*?)', flags=re.I)
# NOTE : column numbers ARE HARDCODED
#Authors: offset 2
#Title: offset 0
#Source: meh ... complicated 8 or 11 + 13
#Year: offset 4
#Keywords: 17
	for i, line in enumerate(sourceCSV):
		if not i:
			#destCSV.writerow(line)
			for j in range(len(line)):
				line[j] = prefix+line[j]
			for j in normalized_columns:
				line.append(prefix+j)
			destCSV.writerow(line)
		else:
			author = line[2]
			if author[-1] == ';':
				author = author[:-1]
			line.append(author)
			line.append(line[0])
			#Source
			if line[8] != '':
				line.append(line[8])
			else:
				line.append(line[11]+' '+line[13])
			line.append(line[4])
			line.append(line[17])
			destCSV.writerow(line)
#f.close()
#g.close()
#h.close()
print("Done")
