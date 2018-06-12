import csv
import re
import sys

# /!\ This code IS **TAB INDENTED** /!\

# Filter notices through keywords regex.

regex = re.compile('(?:.*?)(?:\\W|^)(?:(?:russ(?:i)?e(?!l))|(?:sovi[eé]t)|(?:urss(?!a)))(?:.*?)', flags=re.I)

if len(sys.argv) < 3:
    print('Usage: '+sys.argv[0]+' [infile] [outfile]')
    sys.exit()

#f = open(sys.argv[1], 'r')
#g = open(sys.argv[2], 'w')
with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
    reader = csv.reader(f, delimiter=';', quotechar='"')
    writer = csv.writer(g, delimiter=';', quotechar='"')
    for line in reader:
        #print(line[2])
        if regex.match(line[0]) is not None or regex.match(line[2]) is not None:
            writer.writerow(line)
#g.close()
#f.close()
