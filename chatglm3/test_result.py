from pathlib import Path
from typing import Annotated, Union

import typer
import json

def test_stat_acc(test_file, output_file):
    f = open(test_file, 'r', encoding = 'utf_8')
    map_input = {}
    for each in f:
        jdata = json.loads(each)
        prompt = jdata['conversations'][0]['content']
        prompt = prompt.split('\n')[-1]
        sql =  jdata['conversations'][1]['content']
        if prompt in map_input:
            print(prompt)
        map_input[prompt] = sql
    f_out = open(output_file, 'r', encoding = 'utf_8')
    r = 0
    f = 0
    for each in f_out:
        jdata = json.loads(each)
        prompt = jdata['conversations'][0]['content']
        prompt = prompt.split('\n')[-1]
        sql =  jdata['conversations'][1]['content']
        if prompt in map_input and map_input[prompt] == sql:
            r += 1
            #print("1", prompt, sql)
        else:
            f += 1
            print(f, prompt, '|', sql, '|', map_input[prompt])
    print(r/len(map_input), r, len(map_input))


def test_stat(test_file, output_file, error_file, fix_file, case_file):
    f = open(test_file, 'r', encoding = 'utf_8')
    map_input = {}
    for each in f:
        jdata = json.loads(each)
        prompt = jdata['conversations'][0]['content']
        prompt = prompt.split('\n')[-1]
        sql =  jdata['conversations'][1]['content']
        map_input[prompt] = sql
    map_out = {}
    f_out = open(output_file, 'r', encoding = 'utf_8')
    f_err = open(error_file, 'w', encoding = 'utf_8')
    f_case = open(case_file, 'w', encoding = 'utf_8')
    r = 0
    for each in f_out:
        jdata = json.loads(each)
        prompt = jdata['conversations'][0]['content']
        prompt = prompt.split('\n')[-1]
        sql =  jdata['conversations'][1]['content']
        if map_input[prompt] == sql:
            r += 1
            #print("1", prompt, sql)
        else:
            print("0", prompt, sql, map_input[prompt])
        map_out[prompt] = sql
        if map_input[prompt] != sql:
            data ={
                "conversations": [
                    {"role": "user",
                    "content": "{}{}".format('请将下文解析成BCC检索式：\n', prompt)
                        }, 
                    {"role": "assistant", 
                        "content": "{}".format(map_out[prompt])
                        },
                    {"role": "system", 
                        "content": "{}".format(map_input[prompt])
                        }
                    ]
                }
            item = json.dumps(data, ensure_ascii=False)
            f_err.write("{}\n".format(item))
        else:
            data ={
                "conversations": [
                    {"role": "user",
                    "content": "{}{}".format('请将下文解析成BCC检索式：\n', prompt)
                        }, 
                    {"role": "assistant", 
                        "content": "{}".format(map_out[prompt])
                        },
                    {"role": "system", 
                        "content": "{}".format(map_input[prompt])
                        }
                    ]
                }
            item = json.dumps(data, ensure_ascii=False)
            f_case.write("{}\n".format(item))

    f_fix = open(fix_file, 'r', encoding = 'utf_8')
    for each in f_fix:
        item = each.strip()
        f_case.write("{}\n".format(item))

    print(r/len(map_input), r, len(map_input))


if __name__ == '__main__':
    # test_stat('./chatglm3/dataset_glm_tongyi/bcc_test_case.json', './chatglm3/dataset_glm_tongyi/bcc_test_case_out.json', './chatglm3/dataset_glm_tongyi/bcc_test_err.json', './chatglm3/dataset_glm_tongyi/bcc_test_fix.json', './chatglm3/dataset_glm_tongyi/bcc_test_case.json')
    test_stat_acc('./chatglm3/dataset_glm_tongyi/bcc_test_case.json','./chatglm3/dataset_glm_tongyi/bcc_test_case_out.json')