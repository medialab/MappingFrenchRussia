import csv, sys, re, json
import networkx as nx

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destGEXF]')

    suject_regex = re.compile(r'(.+?\s?(?:\(.*?\))?)(?:,|$)')
    participants_regex = re.compile(r'([A-Z]*)\\,(.*?)(?:,|$)')
    G = nx.Graph()
    subject_set = set()
    participants_set = set()
    with open(sys.argv[1], 'r') as f:
        reader = csv.reader(f)
        for line_num, record in enumerate(reader):
            #print(line_num, record)
            if line_num:
                packed_subjects = record[0]
                packed_participants = record[1]
                for subject in suject_regex.findall(packed_subjects):
                    G.add_node(subject, nodetype='S')
                    subject_set.add(subject)
                    for category, participant in participants_regex.findall(packed_participants):
                        G.add_node(participant, nodetype=category)
                        participants_set.add(participant)
                        G.add_edge(participant, subject)

    nx.write_gexf(G, sys.argv[2])
    print(json.dumps(list(subject_set), indent=1))
    print(json.dumps(list(participants_set), indent=1))