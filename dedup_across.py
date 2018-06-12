import csv, sys

# 5 notices BnF sans auteur no titre
# checkpoint
# 4b3e332101e8723bf0260f7bc76b3fcb
if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('USAGE : ' + sys.argv[0] + '[srcMfr] [dedupBetweenDbMfrCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        reader = csv.reader(f)
        writer = csv.writer(g)
        fused_columns = [11]
        merged_startpoint = 12
        sig_dict = {}
        for not_header, record in enumerate(reader):
            if not not_header:
                writer.writerow(record)
                continue
            sig = record[0]
            if sig not in sig_dict:
                sig_dict[sig] = record
            else:
                for i in fused_columns:
                    sig_dict[sig][i] += '|'+record[i]
                for i in range(merged_startpoint, len(record)):
                    if record[i] is not None and record[i] != "":
                        sig_dict[sig][i] = record[i]
        #print(sig_dict)
        for _, record in sig_dict.items():
            writer.writerow(record)
