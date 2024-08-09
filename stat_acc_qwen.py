import os
import json
import pandas as pd

def conv_log_cvs(test_filename, result_filename, acc_filename):
    f_test = open(test_filename, 'r', encoding="utf-8")
    f_result = open(result_filename, 'r', encoding="utf-8")
    f_acc = open(acc_filename, 'w', encoding='utf_8_sig')
    f_acc.write("{},{},{},{},{}\n".format("query","ground","type","result","correct"))
    j_test = json.load(f_test)
    j_result = json.load(f_result)
    for i in range(len(j_test)):
        if j_test[i]['conversations'][1]['value'] != j_result[i]['conversations'][1]['value']:
            print(j_test[i]['conversations'][0]['value'].split('\n')[1].replace(',', '，').replace('=', '＝'), j_result[i]['conversations'][1]['value'])
            f_acc.write("{},{},{},{},{}\n".format(j_test[i]['conversations'][0]['value'].split('\n')[1].replace(',', '，').replace('=', '＝'), j_test[i]['conversations'][1]['value'], j_test[i]['conversations'][0]['type'], j_result[i]['conversations'][1]['value'].replace(',', '，').replace('=', '＝'), ''))
    pass

def stat_acc(test_filename, result_filename, acc_filename):
    
    map_test = {}
    map_type = {}
    map_acc_right = {}
    map_acc_total = {}
    f_test = open(test_filename, 'r', encoding="utf-8")
    f_result = open(result_filename, 'r', encoding="utf-8")
    df = pd.read_csv(acc_filename)
    map_ea = {}

    j_test = json.load(f_test)
    j_result = json.load(f_result)

    for i in range(len(df)):
        try:
            type = int(df['type'][i])
            correct = df['correct'][i]
            if type > 100:
                type -= 100
            type = str(type)
            if  not pd.isnull(correct):
                map_ea[type] = map_ea.get(type, 0) + 1
                map_ea['0']  = map_ea.get('0', 0) + 1
        except:
            pass
    print(map_ea)
        
    for each in j_test:
        j_data = each
        map_test[j_data['conversations'][0]['value']] = j_data['conversations'][1]['value']
        map_type[j_data['conversations'][0]['value']] = j_data['conversations'][0]['type']
    f_test.close()
    total_8 = 0
    for each in j_result:
        j_data = each
        match = j_data['conversations'][1]['value'].strip() == map_test[j_data['conversations'][0]['value']].strip()
        type = map_type[j_data['conversations'][0]['value']]
        type = type[-1]
        if type == '8':
            type = '7'
        if match:
            map_acc_right[type] = map_acc_right.get(type, 0) + 1
        map_acc_total[type] = map_acc_total.get(type, 0) + 1
        if type != '7':
            if match:
                map_acc_right['0'] = map_acc_right.get('0', 0) + 1
            map_acc_total['0'] = map_acc_total.get('0', 0) + 1
        else:
            total_8 += 1
            if not match:
                print(j_data['conversations'][0]['value'], j_data['conversations'][1]['value'])
                
    f_test.close()

    for each in ['1','2','3','4','5','6','7','0']:
        print(each, '{:.2%}'.format(map_acc_right[each] / map_acc_total[each]), map_acc_right[each], map_acc_total[each])
    
    for each in ['1','2','3','4','5','6','0']:
        print(each, '{:.2%}'.format((map_acc_right[each] + map_ea[each]) / map_acc_total[each]), map_acc_right[each] + map_ea[each], map_acc_total[each])
    
    for each in ['1','2','3','4','5','6','0']:
        print('{:.2%}'.format(map_acc_right[each] / map_acc_total[each]))
    
    for each in ['1','2','3','4','5','6','0']:
        print('{:.2%}'.format((map_acc_right[each] + map_ea[each]) / map_acc_total[each]))
    print(total_8)
if __name__ == '__main__':
    # conv_log_cvs('./qwen/bcc_qwen_tongyi/bcc_test.json', './qwen/bcc_qwen_tongyi/bcc_test_out.json', './data/qwen_acc_ea.csv')
    stat_acc('./qwen/bcc_qwen_tongyi/bcc_test.json', './qwen/bcc_qwen_tongyi/bcc_test_out.json', './data/qwen_acc_ea_result.csv')
    # conv_log_cvs('./log/qwen_log.txt', './data/qwen_loss.csv', './data/qwen_rate.csv')