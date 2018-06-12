import csv, sys, json

def thesis_iterator(thesis_matrix):
    """Iterate over MFR theses.fr CSV dataset
    (aka two rows per record: one for thesis director, one for thesis author).
    """
    dedup_line = True
    for line_num, record in enumerate(thesis_matrix):
        if line_num and dedup_line:
            #directors_list = record[0].lower().split('***')
            director = record[0]
            year = int(record[23])
            topic_list = record[14]
            yield (author, director, year, topic_list)
        if not dedup_line:
            author = record[0]
        dedup_line = not dedup_line

def minimal_topic_dispersion_yearly(f):
    """Compute the number of topics per year."""
    year_dict = {}
    for author, director, year, topic_list in thesis_iterator(f):
        if year not in year_dict:
            year_dict[year] = set()
        for topic in topic_list.split('***'):
            year_dict[year].add(topic)

    yield ['Year', 'Number of Topics']
    for year, topic_set in year_dict.items():
        yield [year, len(topic_set)]

def topic_dispersion_yearly(f):
    """Compute the topics frequences per year."""
    year_dict = {}
    for author, director, year, topic_list in thesis_iterator(f):
        if year not in year_dict:
            year_dict[year] = {}
        for topic in topic_list.split('***'):
            if topic not in year_dict[year]:
                year_dict[year][topic] = 0
            year_dict[year][topic] += 1

    yield ['Year', 'Topic', 'Topic freq']
    for year, topic_dict in year_dict.items():
        for topic_name, topic_freq in topic_dict.items():
            yield [year, topic_name, topic_freq]

def topic_with_director_dispersion(f):
    """Compute for the given thesis subject the directors count."""
    topic_dict = {}
    for author, director, year, topic_list in thesis_iterator(f):
        for topic in topic_list.split('***'):
            if topic not in topic_dict:
                topic_dict[topic] = set()
            topic_dict[topic].add(director)

    yield ['Topic', 'Number of directors']
    for topic, dir_set in topic_dict.items():
        yield [topic, len(dir_set)]

def director_with_topic_dispersion(f):
    """Compute for the given director the thesis subjects count."""
    director_dict = {}
    for author, director, year, topic_list in thesis_iterator(f):
        if director not in director_dict:
            director_dict[director] = set()
        for topic in topic_list.split('***'):
            director_dict[director].add(topic)

    yield ['Director', 'Number of topics']
    for director, topic_set in director_dict.items():
        yield [director, len(topic_set)]

def global_year_director_topic_dispersion(f):
    """Compute for each director each year the topics and their occurences."""
    year_dict = {}
    for author, director, year, topic_list in thesis_iterator(f):
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

    yield ['Year', 'Director', 'Topics', 'Topic Frequences', 'Number of topics']
    for year, director_dict in year_dict.items():
        for director_name, topic_info in director_dict.items():
            topics_piped = '|'.join(topic_info[0])
            freqs_piped = '|'.join(map(str, topic_info[1]))
            topic_number = len(topic_info[0])
            yield [year, director_name, topics_piped, freqs_piped, topic_number]

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        reader = csv.reader(f)
        writer = csv.writer(g)
        stat_func = topic_with_director_dispersion
        for record in stat_func(reader):
            writer.writerow(record)