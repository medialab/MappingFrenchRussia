import sys
import csv

# /!\ This code IS **TAB INDENTED** /!\

# Make a block matrix style CSV to merge the different datasets.

taille_arg = len(sys.argv)
if taille_arg < 2:
    print('Usage: '+sys.argv[0]+' [list of csv] [destination CSV]')
    sys.exit()

srcFiles = []
srcCSV = []
common_header = ['StdAuteur', 'StdTitre', 'StdSource', 'StdAnnée', 'StdMots-clés']
common_header_size = len(common_header)
for i in range(taille_arg-2):
    srcFiles.append(open(sys.argv[i+1], 'r'))
    srcCSV.append(csv.reader(srcFiles[i], delimiter=',', quotechar='"'))
destFile = open(sys.argv[taille_arg-1], 'w')
destCSV = csv.writer(destFile, delimiter=',', quotechar='"')
#print(srcFiles)
#print(sys.argv[taille_arg-1])
#sys.exit()

previous_header_size = common_header_size
current_header_size = 0
common_header_start_in_file = 0
final_data_lines = [common_header]
for i, csvfile in enumerate(srcCSV):
    if not i:
        for j, csvline in enumerate(csvfile):
            if not j:
                current_header_size = len(csvline)
                common_header_start_in_file = len(csvline)-common_header_size
                final_data_lines[0]+=csvline
            else:
                tmp_line = []
                for h in range(previous_header_size):
                    tmp_line+=['']
                for h, csvfield in enumerate(csvline):
                    tmp_line.append(csvfield)
                    if h >= common_header_start_in_file:
                        #print(csvfield)
                        tmp_line[h-common_header_start_in_file] = csvfield
                final_data_lines.append(tmp_line)
    else:
        for j, csvline in enumerate(csvfile):
        # I. Get header & complete previous data
            if not j:
                current_header_size = len(csvline)
                common_header_start_in_file = len(csvline)-common_header_size
                final_data_lines[0]+=csvline
                for csvfield in csvline:
                #    final_data_lines[0].append(csvfield)
                    for h in range(len(final_data_lines)-1):
                        final_data_lines[h+1]+=['']
        # II. Add current data
            else:
                tmp_line = []
                for h in range(previous_header_size):
                    tmp_line+=['']
                for h, csvfield in enumerate(csvline):
                    tmp_line.append(csvfield)
                    if h >= common_header_start_in_file:
                        tmp_line[h-common_header_start_in_file] = csvfield
                final_data_lines.append(tmp_line)
    previous_header_size += current_header_size
#print(srcFiles)
for i in range(taille_arg-2):
    srcFiles[i].close()
#print(final_data_lines[0])
for i in final_data_lines:
    destCSV.writerow(i)

destFile.close()
print("Done")
