import csv, sys

"""Compute Subjects-Publication matrix (a column per subject, a row per publication)
with subjects list as first argument, then publication CSV and finally the
CSV to be written."""

if __name__ == '__main__':
    if len(sys.argv) < 4:
        sys.exit('USAGE : '+sys.argv[0]+' [ElementsList] [PublicationsCSV] [MatrixCSV]')
    with open(sys.argv[1], 'r') as element_list, open(sys.argv[2], 'r') as f, open(sys.argv[3], 'w') as g:
        global_keywords_list = [line[0].strip() for line in csv.reader(element_list)]
        #print(keywords_list)
        reader = csv.reader(f)
        matrix = csv.writer(g)
        record_dict = {}
        for record in reader:
            local_keywords_list = record[4].split(' // ')
            unique_triplet = (record[0], record[1], record[3]) # Author, title, year
            record_dict[unique_triplet] = [0 for i in global_keywords_list]
#            print(keywords_list)
            for keyword in local_keywords_list:
                #kwd_string = keyword
                for element in keyword.split('--'):
                    kwd_string = element.strip()
                    if kwd_string != "":
                        record_dict[unique_triplet][global_keywords_list.index(kwd_string)] = 1

        matrix.writerow(global_keywords_list)
        for _, matrix_row in record_dict.items():
            matrix.writerow(matrix_row)
            print(_)
