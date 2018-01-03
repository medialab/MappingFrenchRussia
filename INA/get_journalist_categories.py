import csv, sys, re

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destCSV]')
    anchor = "Journal télévisé"
    #anchor = "Journal parlé"
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        participants_regex = re.compile(r'([A-Z]*)\\,(.*?)(?:,(?=[\w\[])|$)')
        reader = csv.reader(f)
        writer = csv.writer(g)
        dedup_dict = {}
        for line_num, record in enumerate(reader):
            if not line_num:
                writer.writerow([anchor, 'Nom', 'CAT=JOU'])
            else:
                cat = 'O' if anchor in record[0] else 'N'
                for category, participant in participants_regex.findall(record[2]):
                    jou = 'O' if "JOU" == category else "N"
                    key_tuple = (cat, participant)
                    if jou == "O" or (jou == "N" and key_tuple not in dedup_dict):
                        dedup_dict[key_tuple] = jou
        for (cat, name), jou in dedup_dict.items():
            writer.writerow([cat, name, jou])
        #print(len(dedup_dict))
