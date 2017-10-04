import sys
import csv
import re
if len(sys.argv) < 4:
	print('Usage: '+sys.argv[0]+' [source] [destination] [trad]')
	sys.exit()

with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g, open(sys.argv[3], 'w') as h:
#f = open(sys.argv[1], 'r')
#g = open(sys.argv[2], 'w')
#h = open(sys.argv[3], 'w')
	sourceCSV = csv.reader(f, delimiter=',', quotechar='"')
	destCSV = csv.writer(g, delimiter=',', quotechar='"')
	tradCSV = csv.writer(h, delimiter=',', quotechar='"')
	regex = re.compile('(?:.*?)(?:\\W|^)(?:(?:russ(?:i)?e)|(?:sovi[eé]t)|(?:urss(?!a)))(?:.*?)', flags=re.I)
# NOTE : column numbers ARE HARDCODED
#trad: 5
#sujet 43
# 41-42
	for i, line in enumerate(sourceCSV):
		if not i:
			destCSV.writerow(line)
			tradCSV.writerow(line)
		else:
			if regex.match(line[43]) is not None or regex.match(line[41]) is not None:
				destCSV.writerow(line)
				if 'trad' in line[42].split('/')[-1] or line[5] != '':
					tradCSV.writerow(line)
#f.close()
#g.close()
#h.close()
print("Done")
