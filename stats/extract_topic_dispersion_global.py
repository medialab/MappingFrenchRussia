import csv, sys, json
#from operator import itemgetter

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        reader = csv.reader(f)
        writer = csv.writer(g)
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
                if director not in year_dict[year]:
                    year_dict[year][director] = ([], []) # first is 
                for topic in topic_list.split('***'):
                    if topic not in year_dict[year][director][0]:
                        year_dict[year][director][0].append(topic)
                        year_dict[year][director][1].append(1)
                    else:
                        year_dict[year][director][1][\
                        year_dict[year][director][0].index(topic)\
                        ] += 1

            if not dedup_line:
                author = record[0]
            dedup_line = not dedup_line

        writer.writerow(['Year', 'Director', 'Topics', 'Topic Frequences', 'Number of topics'])
        for year, director_dict in year_dict.items():
            for director_name, topic_info in director_dict.items():
                topics_piped = '|'.join(topic_info[0])
                freqs_piped = '|'.join(map(str, topic_info[1]))
                topic_number = len(topic_info[0])
                writer.writerow([year, director_name, topics_piped, freqs_piped, topic_number])
#            print(year, ',', len(item[0]), ',', len(item[1]), sep='')
#            writer.writerow([year, len(item[0]), len(item[1])])
