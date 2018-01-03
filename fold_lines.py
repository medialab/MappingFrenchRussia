import csv, sys

"""Fold the contiguous splitted lines
(a line is considered splitted if the first column is the only non-empty one).
"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        folded_record = []
        reader = csv.reader(f)
        writer = csv.writer(g)
        for not_header, record in enumerate(reader):
            if not not_header:
                #writer.writerow(record)
                folded_record = record
            else:
                is_same = True
                i = 1
                while i < len(record) and is_same:
                    is_same = i == 102 or record[i] == "" or record[i] is None # offset 102 (aka Isidore_ID) bypass, because of probable OR data corruption
                    i += 1
                if is_same:
                    folded_record[0] += (' // ' + record[0]) if record[0] is not None and record[0] != "" else ""
                else:
                    writer.writerow(folded_record)
                    folded_record = record
        # Last record to be folded isn't written yet
        writer.writerow(folded_record)
