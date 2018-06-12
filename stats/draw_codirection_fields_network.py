import csv, sys
import networkx as nx

"""Draw the bipartite codirectors-fields network (thesis dataset)."""

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
        topic_dict = {}
        director_dict = {}
        edge_set = set() #Convention: first director, second topic
        for author, director_list, year, topic_list, standardized_field in thesis_iterator(reader):
            if standardized_field not in topic_dict:
                topic_dict[standardized_field] = 1
            else:
                topic_dict[standardized_field] += 1

            for i, director in enumerate(director_list):
                # This is soooo rude against G ...
                #G.add_node(director, nodetype="d")
                #G.add_node(standardized_field, nodetype="f")
                #G.add_edge(director, standardized_field)
                if director not in director_dict:
                    director_dict[director] = 1
                else:
                    director_dict[director] += 1
                edge_set.add((director, standardized_field))
                for j in range(i+1, len(director_list)):
                    #print(j)
                    edge_set.add((director, director_list[j]))

        for director, nb_thesis in director_dict.items():
            G.add_node(director, nodetype='d', occ = nb_thesis)
        for topic, nb_thesis in topic_dict.items():
            G.add_node(topic, nodetype='f', occ = nb_thesis)
        for source, target in edge_set:
            G.add_edge(source, target)

        nx.write_gexf(G, sys.argv[2])
