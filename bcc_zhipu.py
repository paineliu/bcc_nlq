from zhipuai import ZhipuAI
import json

# https://open.bigmodel.cn/usercenter/apikeys
def get_secret_key(filename):
    f = open(filename)
    line = f.readline()
    items = line.strip().split()
    if len(items) == 2:
        return items[0], items[1]
    else:
        return "", items[0]

def zhipu_bcc_description(secret_id, secret_key, prompt_filename, query_filename, desc_filename):
    client = ZhipuAI(api_key=secret_key)
    f_prompt = open(prompt_filename, encoding='utf_8')
    prompt = f_prompt.read()
    desc_data = []

    f_query =  open(query_filename, encoding='utf_8')
    query_json = json.load(f_query)

    for i in range(0, len(query_json), 200):
        query_str = ''
        for j in range(i, i + 200):
            query_str += query_json[j]['query'] + '\n'

        response = client.chat.completions.create(
            model="glm-4",  # 填写需要调用的模型名称
            messages=[
                {"role": "user", "content": "{}\n{}".format(prompt, query_str)}
            ],
        )

        out_str = response.choices[0].message.content
        out_item = out_str.split('```')
        if len(out_item) == 3:
            out_data = out_item[1][4:]
            json_data = json.loads(out_data)
            desc_data += json_data
            print(json_data)
        

if __name__ == '__main__':
    secret_id, secret_key = get_secret_key('./secret/zhipu.txt')
    zhipu_bcc_description(secret_id, secret_key, './data/prompt.txt', './data/rmrb_query.json', './data/rmrb_description_zhipu.json')
