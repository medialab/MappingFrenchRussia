import csv, sys

"""Get the list of BnF topics and their occurences."""

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        reader = csv.reader(f)
        writer = csv.writer(g)
        keywords_dict = {}
        for record in reader:
            keywords_field = record[4]
            keywords_list = keywords_field.split(' // ')
#            print(keywords_list)
            for keyword in keywords_list:
                kwd_string = keyword
                #for element in keyword.split('--'):
                #    kwd_string = element.strip()
                if kwd_string not in keywords_dict:
                    keywords_dict[kwd_string] = 0
                keywords_dict[kwd_string] += 1

        for keyword, count in keywords_dict.items():
            writer.writerow([keyword, count])