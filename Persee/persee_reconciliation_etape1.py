import sys
import csv
import re

# /!\ This code IS **TAB INDENTED** /!\

# Add standard (standard as "common for all the datasets") fields with proper formatting.

if len(sys.argv) < 3:
	print('Usage: '+sys.argv[0]+' [source] [destination]')
	sys.exit()

with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
	prefix = 'Persee_'
	normalized_columns = ('StdAuteur', 'StdTitre', 'StdSource', 'StdAnnée', 'StdMots-clés')
#f = open(sys.argv[1], 'r')
#g = open(sys.argv[2], 'w')
#h = open(sys.argv[3], 'w')
	sourceCSV = csv.reader(f, delimiter=',', quotechar='"')
	destCSV = csv.writer(g, delimiter=',', quotechar='"')
	#regex = re.compile('(?:.*?)(?:\\W|^)(?:(?:russ(?:i)?e)|(?:sovi[eé]t)|(?:urss(?!a)))(?:.*?)', flags=re.I)
# NOTE : column numbers ARE HARDCODED
#Authors: offset 1
#Title: offset 2
#Source: 6
#Year: offset 4
#Keywords: None
	for i, line in enumerate(sourceCSV):
		if not i:
			#destCSV.writerow(line)
			for j in range(len(line)):
				line[j] = prefix+line[j]
			for j in normalized_columns:
				line.append(prefix+j)
			destCSV.writerow(line)
		else:
			#Author trick : remove role
			authors = line[1].split(' // ')
			author_line = ''
			one_author = ''
			for j in authors[0].split('-')[:-1]:
				author_line += j
			one_author_split = re.split("([a-zA-Z\-_ ']+?)\.(.*)",author_line)
			if len(one_author_split) > 1:
				author_line = one_author_split[1]+','+one_author_split[2]
			#print(author_line)
			for j in range(len(authors)-1):
				author_line += ' // '
				one_author = ''
				for h in authors[j+1].split('-')[:-1]:
					one_author += h
				one_author_split = re.split("([a-zA-Z\-_ ']+?)\.(.*)",one_author)
				if len(one_author_split) > 1:
					author_line += one_author_split[1]+','+one_author_split[2]
				else:
					author_line += one_author
			line.append(author_line)
			#line.append(line[1])
			line.append(line[2])
			line.append(line[6])
			line.append(line[4])
			line.append('')
			destCSV.writerow(line)
#f.close()
#g.close()
#h.close()
print("Done")
