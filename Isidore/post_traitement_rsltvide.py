import sys

if len(sys.argv) < 3:
	print('Usage: '+sys.argv[0]+' [source] [destination]')
	sys.exit()

f = open(sys.argv[1], 'r')
g = open(sys.argv[2], 'w')
for line in f:
	if line != ',\n':
		g.write(line)

g.close()
f.close()
print("Written")