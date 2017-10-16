import csv
import sys

# /!\ This code IS **TAB INDENTED** /!\

# Kick too old notices

if len(sys.argv) < 3:
	print('Usage '+sys.argv[0]+' [source] [dest]')

with open(sys.argv[1],'r') as f, open(sys.argv[2],'w') as g:
#f = open(sys.argv[1],'r')
#g = open(sys.argv[2],'w')
	sourceCSV = csv.reader(f)
	destCSV = csv.writer(g)
	for line in sourceCSV:
		if int(line[4]) >= 1980:
			destCSV.writerow(line)
#f.close()
#g.close()
print('Done')
