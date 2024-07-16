import os
import json

def merge_desc(log_pathname, json_filename):
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
    data2 = sorted(desc_data, key=lambda keys: keys.get("query"), reverse=False)
    f_json = open(json_filename, 'w', encoding='utf_8')
    json.dump(data2, f_json, ensure_ascii=False, indent=4)
    f_json.close()

if __name__ == '__main__':

    merge_desc('./log/tongyi', './data/rmrb_desc_tongyi.json')
    merge_desc('./log/zhipu', './data/rmrb_desc_zhipu.json')
    merge_desc('./log/kimi', './data/rmrb_desc_kimi.json')