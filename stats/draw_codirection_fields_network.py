import csv, sys
import networkx as nx

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
            standardized_field = record[13]
            if '***' in director:
                director_list = director.split('***')
                yield (author, director_list, year, topic_list, standardized_field)
        if not dedup_line:
            author = record[0]
        dedup_line = not dedup_line

# 13
if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destGEXF]')
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        G = nx.Graph()
        for author, director_list, year, topic_list, standardized_field in thesis_iterator(reader):
            for director in director_list:
                # This is soooo rude against G ...
                G.add_node(director, nodetype="d")
                G.add_node(standardized_field, nodetype="f")
                G.add_edge(director, standardized_field)

        nx.write_gexf(G, sys.argv[2])
