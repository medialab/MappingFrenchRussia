import csv, sys, json
from operator import itemgetter

"""Get the number of thesis directors and authors per year."""

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        reader = csv.reader(f)
        writer = csv.writer(g)
        column_dict = {}
        parent_dict = {}
        year_dict = {}
        dedup_line = True
        for line_num, record in enumerate(reader):
            if line_num and dedup_line:
                #directors_list = record[0].lower().split('***')
                director = record[0]
                year = int(record[23])
                #topic = record[14]
                # TODO topic dispersion
#                for director in directors_list:
                if director not in column_dict:
                    column_dict[director] = []
                column_dict[director].append((author, year))

                if year not in year_dict:
                    year_dict[year] = (set(), set())
                year_dict[year][0].add(director)
                year_dict[year][1].add(author)

                if parent_dict.get(author, "") == "":
                    parent_dict[author] = director
                if director not in parent_dict:
                    parent_dict[director] = ""

            if not dedup_line:
                author = record[0]
            dedup_line = not dedup_line
#        rslt = []
        writer.writerow(['Year', 'Director number', 'Author number'])
        for year, item in year_dict.items():
#            print(year, ',', len(item[0]), ',', len(item[1]), sep='')
            writer.writerow([year, len(item[0]), len(item[1])])
