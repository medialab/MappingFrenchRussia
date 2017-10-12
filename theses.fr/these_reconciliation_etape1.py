import sys
import csv
import re
if len(sys.argv) < 3:
	print('Usage: '+sys.argv[0]+' [source] [destination]')
	sys.exit()

with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
	prefix = 'Theses_'
	normalized_columns = ('StdAuteur', 'StdTitre', 'StdSource', 'StdAnnée', 'StdMots-clés')
#f = open(sys.argv[1], 'r')
#g = open(sys.argv[2], 'w')
#h = open(sys.argv[3], 'w')
	sourceCSV = csv.reader(f, delimiter=',', quotechar='"')
	destCSV = csv.writer(g, delimiter=',', quotechar='"')
	#regex = re.compile('(?:.*?)(?:\\W|^)(?:(?:russ(?:i)?e)|(?:sovi[eé]t)|(?:urss(?!a)))(?:.*?)', flags=re.I)
# NOTE : column numbers ARE HARDCODED
#Authors: offset 17 & offset 14 (duplicate lines)
#Title: offset 2
#Source: offset 18 + 27
#Year: offset 21
#Keywords: 6
	source_size = 0
	for i, line in enumerate(sourceCSV):
		#print(i)
		if not i:
			#destCSV.writerow(line)
			source_size = len(line)
			for j in range(len(line)):
				line[j] = prefix+line[j]
			for j in normalized_columns:
				line.append(prefix+j)
			destCSV.writerow(line)
			#print(line)
		else:
			#print(line, source_size)
			doc_words = line[17].split(' ')
			if len(doc_words) == 2:
				line.append(doc_words[1]+' '+doc_words[0])
			else:
				line.append(' '.join(doc_words))
			line.append(line[2])
			line.append(line[18]+', '+line[27])
			line.append(line[21])
			line.append(line[6].replace('***', ' // '))
			destCSV.writerow(line)
			line[source_size] = line[14]
			destCSV.writerow(line)
#f.close()
#g.close()
#h.close()
print("Done")
