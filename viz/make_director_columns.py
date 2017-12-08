import csv, sys, json
from operator import itemgetter

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destJSON]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        reader = csv.reader(f)
#        writer = csv.writer(g)
        column_dict = {}
        parent_dict = {}
        dedup_line = True
        for line_num, record in enumerate(reader):
            if line_num and dedup_line:
                #directors_list = record[0].lower().split('***')
                director = record[0]
                year = record[23]
#                for director in directors_list:
                if director not in column_dict:
                    column_dict[director] = []
                column_dict[director].append((author, int(year)))

                if parent_dict.get(author, "") == "":
                    parent_dict[author] = director
                if director not in parent_dict:
                    parent_dict[director] = ""

            if not dedup_line:
                author = record[0]
            dedup_line = not dedup_line
        rslt = []
        for key, author_year_list in column_dict.items():
#            sorted_list = sorted(author_year_list, key=itemgetter(1))
 #           for author, year in sorted_list:
            for author, year in author_year_list:
                # Finding the oldest ancestor
                ancestor = author
                while parent_dict.get(ancestor, "") != "":
                    ancestor = parent_dict[ancestor]
                rslt.append({'ancestor':ancestor, 'director':key, 'author':author, 'year':year})
        rslt = sorted(rslt, key = itemgetter('ancestor', 'director', 'year', 'author'))
        json.dump(rslt, g, indent=1)
#            writer.writerow([key]+sorted_list)
