import csv, sys, json
from operator import itemgetter

"""Get the list of escaped PhD (aka there is no signs of academic
publication after the thesis, so it is probably someone that didn't
follow the academic path)."""

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV]')
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
#        writer = csv.writer(g)
        thesis_publicable_author = set()
        publication_set = set()

        dedup_line = True
        author = ""
        for line_num, record in enumerate(reader):
            name_field = record[0]
            year = record[2]
            thesis_id = record[3]

            if thesis_id != "":
                if line_num and dedup_line and int(year) < 2014:# Don't take into account recent thesis.
                    #director = record[0]
    #                for director in directors_list:
                    thesis_publicable_author.add(author)

                if not dedup_line:
                    author = name_field
                dedup_line = not dedup_line
            else:
                for pub_author in name_field.split(' // '):
                    publication_set.add(pub_author)

        print(len(publication_set), len(thesis_publicable_author), file=sys.stderr)
        for i in thesis_publicable_author - publication_set:
            print(i)
