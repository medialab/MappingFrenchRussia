import csv, sys

if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit('USAGE : '+sys.argv[0]+' [srcCSV] [destCSV]')
    with open(sys.argv[1], 'r') as f, open(sys.argv[2], 'w') as g:
        reader = csv.reader(f)
        writer = csv.writer(g)
        start_year = 1985
        end_year = 2018
        time_studied_year_weight_dict = {}
        time_studied_columns = set()
        catched_line = True
        year = 0
        time_interval = [0,0]
        for line_num, record in enumerate(reader):
            thesis_id = record[2]
            if line_num:
                year = int(record[1].split('-')[-1].split(' // ')[0])
                time_interval = [int(date.split(' // ')[0]) for date in record[0].split('_')] if record[0] != 'Paléolithique' else -1
            #print(time_interval)

            # Take the first thesis record per thesis (there is two records per thesis)
            # and all the BnF records
            catched_line = thesis_id == "" or (not catched_line and line_num)
            if catched_line:
                if time_interval == -1:
                    time_studied_columns.add(-1)

                    if -1 not in time_studied_year_weight_dict:
                        time_studied_year_weight_dict[-1] = {}
                    if year not in time_studied_year_weight_dict[-1]:
                        time_studied_year_weight_dict[-1][year] = 0

                    time_studied_year_weight_dict[-1][year] += 100
                else:
                    local_start = time_interval[0]
                    local_stop = 1+time_interval[-1]
                    ### data DEBUG on the fly ###
                    #if local_stop > 2018:
                    #    print(time_interval, thesis_id, record[3])
                    #############################
                    local_weight = 100/(local_stop-local_start)
                    for weighted_time in range(local_start, local_stop):
                        #print(time_interval, weighted_time)
                        time_studied_columns.add(weighted_time)

                        if weighted_time not in time_studied_year_weight_dict:
                            time_studied_year_weight_dict[weighted_time] = {}
                        if year not in time_studied_year_weight_dict[weighted_time]:
                            time_studied_year_weight_dict[weighted_time][year] = 0

                        time_studied_year_weight_dict[weighted_time][year] += local_weight
                    #print(time_studied_year_weight_dict[year])

        columns_list = sorted(list(time_studied_columns))
        #print(columns_list)
        writer.writerow(['Time']+[i for i in range(start_year, end_year+1)])
        for time in columns_list:
            #print(year)
            year_weights = [time_studied_year_weight_dict[time].get(i, 0) for i in range(start_year, end_year+1)]
            writer.writerow([time]+year_weights)
