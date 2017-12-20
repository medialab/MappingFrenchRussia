import csv, sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV) [destCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        reader = csv.reader(f)
        writer = csv.writer(g)
        date_dict = {}
        topic_set = set()
        for line_num, record in enumerate(reader):
            if line_num:
                topic = record[1]
                year = int(record[0])
                if topic not in topic_set:
                    topic_set.add(topic)
                    if year not in date_dict:
                        date_dict[year] = []
                    date_dict[year].append(topic)

        for year, topic_list in date_dict.items():
            for topic in topic_list:
                writer.writerow([year, topic])
