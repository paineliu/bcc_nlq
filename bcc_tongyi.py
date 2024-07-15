import random
from http import HTTPStatus
import dashscope
from dashscope import Generation  # 建议dashscope SDK 的版本 >= 1.14.0
from secret import get_secret_key
import os
import json

def tongyi_bcc_description(secret_id, secret_key, prompt_filename, query_filename, desc_filename, log_pathname):
    dashscope.api_key = secret_key
    f_prompt = open(prompt_filename, encoding='utf_8')
    prompt = f_prompt.read()
    desc_data = []

    os.makedirs(log_pathname, exist_ok=True)

    f_query =  open(query_filename, encoding='utf_8')
    query_json = json.load(f_query)
    step = 40
    for i in range(250, len(query_json), step):
        query_str = ''
        for j in range(i, i + step):
            if j < len(query_json):
                query_str += query_json[j]['query'] + '\n'

        try:
            messages = [{'role': 'user', 'content': "{}\n{}".format(prompt, query_str)}]
            response = Generation.call(model="qwen-turbo",
                                    messages=messages,
                                    # 设置随机数种子seed，如果没有设置，则随机数种子默认为1234
                                    seed=random.randint(1, 10000),
                                    # 将输出设置为"message"格式
                                    result_format='message')
            if response.status_code == HTTPStatus.OK:
                print(response)
            else:
                print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                ))

            out_str = response['output']['choices'][0]['message']['content']
            out_item = out_str.split('```')
            if len(out_item) >= 2:
                print(i)
                out_data = out_item[1][5:]
                log_filename = os.path.join(log_pathname, "tongyi_" + str(i) + ".txt")
                f = open(log_filename, 'w', encoding='utf-8')
                f.write(out_str)
                f.close()
                json_data = json.loads(out_data)
                desc_data += json_data
                f_desc = open(desc_filename, 'w', encoding='utf_8')
                json.dump(desc_data, f_desc, ensure_ascii=False, indent=4)
            
        except:
            pass

if __name__ == '__main__':
    secret_id, secret_key = get_secret_key('./secret/tongyi.txt')
    tongyi_bcc_description(secret_id, secret_key, './data/prompt.txt', './data/rmrb_query.json', './data/rmrb_description_tongyi.json', './log/tongyi')
