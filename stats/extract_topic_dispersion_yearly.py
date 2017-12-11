import csv, sys, json
#from operator import itemgetter

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        reader = csv.reader(f)
        writer = csv.writer(g)
        #column_dict = {}
        #parent_dict = {}
        year_dict = {}
        dedup_line = True
        for line_num, record in enumerate(reader):
            if line_num and dedup_line:
                #directors_list = record[0].lower().split('***')
                director = record[0]
                year = int(record[23])
                topic_list = record[14]

                if year not in year_dict:
                    year_dict[year] = {}
#                if director not in year_dict[year]:
#                    year_dict[year][director] = ([], []) # first is 
                for topic in topic_list.split('***'):
                    if topic not in year_dict[year]:
                        year_dict[year][topic] = 0
                    year_dict[year][topic] += 1

            if not dedup_line:
                author = record[0]
            dedup_line = not dedup_line
#        rslt = []
        writer.writerow(['Year', 'Topic', 'Topic freq'])
        for year, topic_dict in year_dict.items():
            for topic_name, topic_freq in topic_dict.items():
                writer.writerow([year, topic_name, topic_freq])
                #writer.writerow([year, len(topic_dict)])
#            print(year, ',', len(item[0]), ',', len(item[1]), sep='')
#            writer.writerow([year, len(item[0]), len(item[1])])
