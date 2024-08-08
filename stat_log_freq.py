import os
import json
import datetime
import unicodedata
import pandas as pd

def stat_log_freq(log_filename, fix_filename, freq_filename):
        
    df = pd.read_csv(log_filename)
    map_data = {}
    map_add = {}
    for i in range(1, 8):
        map_add[i] = {}
        map_data[i] = {}

    for i in range(len(df)):
        type = df['type'][i]
        query = df['query'][i]
        if type >= 6 and type <10:
            type = 6
        elif type >= 10:
            type = 7
        map_data[type][query] = map_data[type].get(query, 0) + 1
    
    for type in range(1, 8):
        list_sort = sorted(map_data[type].items(), key=lambda d: d[1], reverse=True)
        f = open(freq_filename + '_{}.csv'.format(type), 'w', encoding='utf_8_sig')
        f.write('{},{}\n'.format('query', 'times'))
        for item in list_sort:
            f.write('{},{}\n'.format(item[0], item[1]))
        f.close()
    f_fix = open(fix_filename, encoding='utf-8')
    j_data = json.load(f_fix)
    
    for item in j_data:        
        query = item['query']
        type = int(item['type'])
        if type > 100:
            continue
        if type > 7:
            type = 7
        if query not in map_data[type]:
            map_add[type][query] = map_add[type].get(query, 0) + 1

    for type in range(1, 8):
        list_sort = sorted(map_add[type].items(), key=lambda d: d[1], reverse=True)
        f = open(freq_filename + '_add_{}.csv'.format(type), 'w', encoding='utf_8_sig')
        f.write('{},{}\n'.format('query', 'times'))
        for item in list_sort:
            f.write('{},{}\n'.format(item[0], item[1]))
        f.close()


if __name__ == '__main__':
    stat_log_freq('./data/bcc_log.csv', './data/bcc_query_desc_type_fixed_tongyi.json', './data/bcc_log_stat')
    