from zhipuai import ZhipuAI
import json
import os

from secret import get_secret_key

# https://open.bigmodel.cn/usercenter/apikeys

def zhipu_bcc_description(secret_id, secret_key, prompt_filename, query_filename, desc_filename, log_pathname):
    client = ZhipuAI(api_key=secret_key)
    f_prompt = open(prompt_filename, encoding='utf_8')
    prompt = f_prompt.read()
    desc_data = []

    os.makedirs(log_pathname, exist_ok=True)

    f_query =  open(query_filename, encoding='utf_8')
    query_json = json.load(f_query)
    step = 20
    for i in range(20810, len(query_json), step):
        query_str = ''
        for j in range(i, i + step):
            if j < len(query_json):
                query_str += query_json[j]['query'] + '\n'

        try:
            response = client.chat.completions.create(
                model="glm-4",  # 填写需要调用的模型名称
                messages=[
                    {"role": "user", "content": "{}\n{}".format(prompt, query_str)}
                ],
            )

            out_str = response.choices[0].message.content
            out_item = out_str.split('```')
            if len(out_item) >= 2:
                print(i)
                out_data = out_item[1][5:]
                log_filename = os.path.join(log_pathname, "zhipu_" + str(i) + ".txt")
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
    secret_id, secret_key = get_secret_key('./secret/zhipu.txt')
    zhipu_bcc_description(secret_id, secret_key, './data/prompt.txt', './data/rmrb_query.json', './data/rmrb_description_zhipu.json', './log/zhipu')
