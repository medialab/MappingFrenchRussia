import csv, sys, json
from operator import itemgetter

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV]')
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
#        writer = csv.writer(g)
        thesis_publicable_author = set()
        publication_set = set()

        dedup_line = True
        for line_num, record in enumerate(reader):
            if record[3] != "":
                if line_num and dedup_line and int(record[2]) < 2014:
                    #director = record[0]
    #                for director in directors_list:
                    thesis_publicable_author.add(author)

                if not dedup_line:
                    author = record[0]
                dedup_line = not dedup_line
            else:
                for pub_author in record[0].split(' // '):
                    publication_set.add(pub_author)

        print(len(publication_set), len(thesis_publicable_author), file=sys.stderr)
        for i in thesis_publicable_author - publication_set:
            print(i)
