import os
import json
import pandas as pd
from stat_bcc_query import get_query_type6


def merge_desc(query_filename, log_pathname, json_filename):
    df = pd.read_csv(query_filename)
    map_query_type = {}

    for i in range(len(df)):
        query = df['query'][i]
        type = df['type'][i]
        map_query_type[query] = type
        if '+' in query:
            query2 = query.replace('+', ' ')
            map_query_type[query2] = type

    paths = os.walk(log_pathname)
    desc_data= []
    for path, dir_lst, file_lst in paths:
        for file_name in file_lst:
            full_name = os.path.join(path, file_name)
            f = open(full_name, encoding='utf_8')
            out_str = f.read()
            out_item = out_str.split('```')
            if len(out_item) >= 2:
                print(full_name)
                out_data = out_item[1][5:]
                try:
                    json_data = json.loads(out_data)
                    desc_data += json_data
                except Exception as e:
                    print(full_name, False)
                    print(e)
            else:
                print(full_name, False)
    desc_data2 = []
    total = 0
    for each in desc_data:
        if not isinstance(each, dict):
            print(each) 
        else:
            if 'description' in each:
                query = each['query']
                #type = map_query_type[each['query']]
                if ',' in query:
                    query = query.replace(',', '，')
                if '"' == query[0]:
                    query = query.strip('"')
                type = get_query_type6(query)
                if type != 0:
                    each['type'] = str(type)
                    # if 'v' in each['description'] or 'a' in each['description']:
                        # print(total, each['query'], each['description'])
                    desc_data2.append(each)
                    total += 1
                else:
                    print(total, each['query'], each['description'])
                
    data2 = sorted(desc_data2, key=lambda keys: keys.get("type"), reverse=False)
    f_json = open(json_filename, 'w', encoding='utf_8')
    json.dump(data2, f_json, ensure_ascii=False, indent=4)
    f_json.close()

def add_fixed(fix_filename, query_filename, out_filename):
    f_query = open(query_filename, 'r', encoding='utf_8')
    desc_data2 = json.load(f_query)
    f_query.close()

    df = pd.read_csv(fix_filename)
    map_query_type = {}

    for i in range(len(df)):
        query = df['query'][i]
        desc = df['respond'][i]
        type = str(df['type'][i])
        data = {'query':query, 'description':desc, 'type':type}
        desc_data2.append(data)
        if '+' in query:
            query2 = query.replace('+', ' ')
            data2 = {'query':query2, 'description':desc, 'type':type}    
            desc_data2.append(data2)

    data2 = sorted(desc_data2, key=lambda keys: keys.get("type"), reverse=False)
    f_json = open(out_filename, 'w', encoding='utf_8')
    json.dump(data2, f_json, ensure_ascii=False, indent=4)
    f_json.close()

    
if __name__ == '__main__':

    merge_desc('./data/bcc_log.csv','./log/tongyi', './data/bcc_query_desc_type_tongyi.json')
    add_fixed('./data/bcc_fixed.csv', './data/bcc_query_desc_type_tongyi.json', './data/bcc_query_desc_type_fixed_tongyi.json')
    # merge_desc('./log/zhipu', './data/rmrb_desc_zhipu.json')
    # merge_desc('./log/kimi', './data/rmrb_desc_kimi.json')