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
        #year_dict = {}
#        director_dict = {}
        topic_dict = {}
        dedup_line = True
        for line_num, record in enumerate(reader):
            if line_num and dedup_line:
                #directors_list = record[0].lower().split('***')
                director = record[0]
                year = int(record[23])
                topic_list = record[14]
#                for director in directors_list:
#                if director not in director_dict:
#                    director_dict[director] = set()
                #column_dict[director].append((author, year))

                #if year not in year_dict:
                 #   year_dict[year] = {}
#                if director not in year_dict[year]:
#                    year_dict[year][director] = ([], []) # first is 
                for topic in topic_list.split('***'):
                    #director_dict[director].add(topic)
                    if topic not in topic_dict:
                        topic_dict[topic] = set()
                    topic_dict[topic].add(director)
                #if parent_dict.get(author, "") == "":
                #    parent_dict[author] = director
                #if director not in parent_dict:
                #    parent_dict[director] = ""

            if not dedup_line:
                author = record[0]
            dedup_line = not dedup_line
#        rslt = []
#        writer.writerow(['Director', 'Number of topics'])
        writer.writerow(['Topic', 'Number of directors'])
#        for director, topic_set in director_dict.items():
        for topic, dir_set in topic_dict.items():
            #writer.writerow([director, len(topic_set)])
            writer.writerow([topic, len(dir_set)])
