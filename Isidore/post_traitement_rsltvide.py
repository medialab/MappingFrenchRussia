import sys

# /!\ This code is **TAB INDENTED** /!\

# Kicks the empty results of given 2-column CSV.

if len(sys.argv) < 3:
    print('Usage: '+sys.argv[0]+' [source] [destination]')
    sys.exit()
with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
#f = open(sys.argv[1], 'r')
#g = open(sys.argv[2], 'w')
    for line in f:
        if line != ',\n':
            g.write(line)

#g.close()
#f.close()
print("Done")
