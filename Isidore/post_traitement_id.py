import sys
import csv

if len(sys.argv) < 4:
	print('Usage: '+sys.argv[0]+' [source] [destination] [id column number]')
	sys.exit()

f = open(sys.argv[1], 'r')
g = open(sys.argv[2], 'w')
sourceCSV = csv.reader(f, delimiter=',', quotechar='"')
destCSV = csv.writer(g, delimiter=',', quotechar='"')
for line in sourceCSV:
	#if line != ',\n':
	#	g.write(line)
	id_text = line[int(sys.argv[3])-1].split(' // ')
	#print(id_text)
	for i in range(len(id_text)):
		if 'http' in id_text[i]:
			line[int(sys.argv[3])-1] = id_text[i]
	destCSV.writerow(line)

g.close()
f.close()
print("Written")