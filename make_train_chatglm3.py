import os
import json

def make_train_dataset(desc_filename, train_pathname):
    
    os.makedirs(train_pathname, exist_ok=True)

    f = open(desc_filename, encoding="utf-8")
    desc_data = json.load(f)

    train_data = []
    test_data = []
    val_data = []
    line_total = 0
    
    for item in desc_data:
        if 'query' in item and 'description' in item:
            query = item['query']
            description = item['description']
            type = item['type']
            data = {
                "conversations": [
                    {
                        "role": "user",
                        "content": "{}{}".format("请将下文解析成BCC检索式：\n", description),
                        "type" :type 
                    }, 
                    {
                        "role": "assistant", 
                        "content": "{}".format(query)
                    }
                ]
            }

            if int(type) <= 6:
                data2 = {
                    "conversations": [
                        {
                            "role": "user",
                            "content": "{}{}".format("请将下文解析成BCC检索式：\n", query),
                            "type": '10' + type
                        },
                        {
                            "role": "assistant",
                            "content": "{}".format(query)
                        }
                    ]
                }
            else:
                data2 = None

            if (line_total % 10) < 8:
                train_data.append(data)
                if data2 is not None:
                    train_data.append(data2)       
            elif (line_total % 10) < 9:
                test_data.append(data)
                if data2 is not None:
                    test_data.append(data2) 
            else:
                val_data.append(data)
                if data2 is not None:
                    val_data.append(data2)
                    
            line_total += 1    

    f = open(os.path.join(train_pathname, "bcc_train.json"), 'w', encoding='utf-8')
    for each in train_data:
        item = json.dumps(each, ensure_ascii=False)
        f.write("{}\n".format(item))
    f.close()

    f = open(os.path.join(train_pathname, "bcc_test.json"), 'w', encoding='utf-8')
    for each in test_data:
        item = json.dumps(each, ensure_ascii=False)
        f.write("{}\n".format(item))
    f.close()

    f = open(os.path.join(train_pathname, "bcc_dev.json"), 'w', encoding='utf-8')
    for each in val_data:
        item = json.dumps(each, ensure_ascii=False)
        f.write("{}\n".format(item))
    f.close()

if __name__ == '__main__':
    make_train_dataset('./data/bcc_query_desc_type_fixed_tongyi.json', './chatglm3/bcc_glm_tongyi')