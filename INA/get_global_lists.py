import csv, sys, re, json
import networkx as nx

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' s1 r2 p3 [srcCSV]')

    suject_regex = re.compile(r'(.+?\s?(?:\(.*?\))?)(?:,|$)')
    participants_regex = re.compile(r'([A-Z]*)\\,(.*?)(?:,|$)')
    G = nx.Graph()
    subject_set = set()
    role_set = set()
    participants_set = set()
    for i in range(4, len(sys.argv)):
        print(sys.argv[i])
        with open(sys.argv[i], 'r') as f:
            reader = csv.reader(f)
            for line_num, record in enumerate(reader):
                #print(line_num, record)
                if line_num:
                    packed_subjects = record[0]
                    packed_participants = record[1]
                    for subject in suject_regex.findall(packed_subjects):
                        subject_set.add(subject)
                        for category, participant in participants_regex.findall(packed_participants):
                            participants_set.add(participant)
                            role_set.add(category)

    with open(sys.argv[1], 'w') as f:
        for key in subject_set:
            f.write(key+'\n')
    with open(sys.argv[2], 'w') as f:
        for key in role_set:
            f.write(key+'\n')
    with open(sys.argv[3], 'w') as f:
        for key in participants_set:
            f.write(key+'\n')