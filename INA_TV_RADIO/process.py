#!/usr/bin/env python3
import csv
import re
import unicodedata
from collections import defaultdict, OrderedDict

# Constants
CSV_FILES = [
    './RADIO.csv',
    './TVNAT.csv',
    './TVREG.csv',
    './TVSAT.csv'
]

FILE = './researchers.txt'

OUTPUT = './result.csv'

# Indices
PERSONS = defaultdict(list)
FINGERPRINT_INDEX = defaultdict(set)
RESEARCHERS = {}

# Helpers
SPLITTER = r',(?=[A-Z]{2,10}\\)'
CLEANER = r'\([^)]+\)'
STRIPPER = r'[,()]'
MULTIPLEXER = r'[\-]'
SQUEEZER = r'\s+'

def remove_accents(input_str):
    nfkd_form = unicodedata.normalize('NFKD', input_str)
    return u''.join([c for c in nfkd_form if not unicodedata.combining(c)])

def parse_gen(gen):
    gen = gen.strip()

    if not gen:
        return []

    tokens = re.split(SPLITTER, gen)

    return [(token.split('\\,')[0], ', '.join(token.split('\\,')[1:])) for token in tokens]

def clean(name):
    return name.split('(')[0].strip()

def fingerprint(name):
    name = name.strip()
    name = name.lower()
    name = remove_accents(name)
    name = re.sub(STRIPPER, '', name)
    name = re.sub(SQUEEZER, ' ', name)
    name = re.sub(MULTIPLEXER, ' ', name)

    tokens = sorted(set(name.split(' ')))

    return ' '.join(tokens)

# Indexing CSV files
for path in CSV_FILES:
    print('Indexing %s' % path)
    with open(path, 'r') as f:
        reader = csv.DictReader(f)

        for line in reader:
            persons = parse_gen(line['gen'])

            for p in persons:
                if p[0] == 'PAR':
                    name = clean(p[1])
                    PERSONS[name].append(line)
                    FINGERPRINT_INDEX[fingerprint(name)].add(name)

# Collecting researchers
with open(FILE, 'r') as f:
    for line in f.readlines():
        line = line.strip()

        RESEARCHERS[line] = fingerprint(line)

# Querying
print('Writing result to CSV file...')
output_file = open(OUTPUT, 'w')
fieldnames = ['researcher'] + list(list(PERSONS.values())[0][0].keys())
writer = csv.DictWriter(output_file, fieldnames=fieldnames)
writer.writeheader()

M = 0
for researcher, fingerprint in RESEARCHERS.items():
    matches = FINGERPRINT_INDEX[fingerprint]

    if matches:
        M += 1

        if len(matches) > 1:

            print('Issue: found %i results for %s:' % (len(matches), researcher))

            for match in matches:
                print('  -> %s' % match)

            print()
            continue

        match = list(matches)[0]
        lines = PERSONS[match]

        for line in lines:
            output_line = OrderedDict()
            output_line['researcher'] = researcher

            for k in line.keys():
                output_line[k] = line[k]

            writer.writerow(output_line)

print('%i matches.' % M)

output_file.close()
