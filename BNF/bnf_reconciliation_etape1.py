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
	prefix = 'BNF_'
	normalized_columns = ('StdAuteur', 'StdTitre', 'StdSource', 'StdAnnée', 'StdMots-clés')
#f = open(sys.argv[1], 'r')
#g = open(sys.argv[2], 'w')
#h = open(sys.argv[3], 'w')
	sourceCSV = csv.reader(f, delimiter=',', quotechar='"')
	destCSV = csv.writer(g, delimiter=',', quotechar='"')
	#regex = re.compile('(?:.*?)(?:\\W|^)(?:(?:russ(?:i)?e)|(?:sovi[eé]t)|(?:urss(?!a)))(?:.*?)', flags=re.I)
# NOTE : column numbers ARE HARDCODED
#Authors: offset 1
#Title: offset 41
#Source: offset 45 + 48
#Year: offset 46
#Keywords: 43
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
			line.append(line[1])
			line.append(line[41])
			line.append(line[45]+' ('+line[49]+')')
			line.append(line[47])
			line.append(line[43])
			destCSV.writerow(line)
#f.close()
#g.close()
#h.close()
print("Done")
