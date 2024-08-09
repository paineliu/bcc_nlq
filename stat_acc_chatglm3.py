import os
import json
import pandas as pd

def conv_log_cvs(test_filename, result_filename, acc_filename):
    
    map_test = {}
    map_type = {}
    map_acc_right = {}
    map_acc_total = {}
    f_test = open(test_filename, 'r', encoding="utf-8")
    f_result = open(result_filename, 'r', encoding="utf-8")
    df = pd.read_csv(acc_filename)
    map_ea = {}

    for i in range(len(df)):
        type = df['type'][i]
        correct = df['correct'][i]
        if type > 100:
            type -= 100
        type = str(type)
        if  not pd.isnull(correct):
            map_ea[type] = map_ea.get(type, 0) + 1
            map_ea['0']  = map_ea.get('0', 0) + 1
    print(map_ea)
        
    for each in f_test:
        j_data = json.loads(each)
        map_test[j_data['conversations'][0]['content']] = j_data['conversations'][1]['content']
        map_type[j_data['conversations'][0]['content']] = j_data['conversations'][0]['type']
    f_test.close()

    for each in f_result:
        j_data = json.loads(each)
        match = j_data['conversations'][1]['content'].strip() == map_test[j_data['conversations'][0]['content']].strip()
        type = map_type[j_data['conversations'][0]['content']]
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
            if not match:
                print(j_data['conversations'][0]['content'], j_data['conversations'][1]['content'])
                
    f_test.close()

    for each in ['1','2','3','4','5','6','7','0']:
        print(each, '{:.2%}'.format(map_acc_right[each] / map_acc_total[each]), map_acc_right[each], map_acc_total[each])
    
    for each in ['1','2','3','4','5','6','0']:
        print(each, '{:.2%}'.format((map_acc_right[each] + map_ea[each]) / map_acc_total[each]), map_acc_right[each] + map_ea[each], map_acc_total[each])
    
    for each in ['1','2','3','4','5','6','0']:
        print('{:.2%}'.format(map_acc_right[each] / map_acc_total[each]))
    
    for each in ['1','2','3','4','5','6','0']:
        print('{:.2%}'.format((map_acc_right[each] + map_ea[each]) / map_acc_total[each]))
    
if __name__ == '__main__':
    conv_log_cvs('./chatglm3/bcc_glm_tongyi/bcc_test.json', './chatglm3/bcc_glm_tongyi/bcc_test_out.json', './data/chatglm3_acc_ea_result.csv')
    # conv_log_cvs('./log/qwen_log.txt', './data/qwen_loss.csv', './data/qwen_rate.csv')