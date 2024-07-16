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
            data ={
                "id": "identity_{}".format(line_total),
                "conversations": [
                    {
                        "from": "user",
                        "value": "{}{}".format("请将下文解析成BCC检索式：\n", description)
                    },
                    {
                        "from": "assistant",
                        "value": "{}".format(query)
                    }
                ]
            }
                    
            if (line_total % 10) < 8:
                train_data.append(data)
            elif (line_total % 10) < 9:
                test_data.append(data)
            else:
                val_data.append(data)
            line_total += 1    

    f = open(os.path.join(train_pathname, "bcc_train.jsonl"), 'w', encoding='utf-8')
    json.dump(train_data, f, ensure_ascii=False, indent=4)
    f.close()

    f = open(os.path.join(train_pathname, "bcc_test.jsonl"), 'w', encoding='utf-8')
    json.dump(test_data, f, ensure_ascii=False, indent=4)
    f.close()

    f = open(os.path.join(train_pathname, "bcc_dev.jsonl"), 'w', encoding='utf-8')
    json.dump(val_data, f, ensure_ascii=False, indent=4)
    f.close()

if __name__ == '__main__':
    make_train_dataset('./data/rmrb_desc_tongyi.json', './data/dataset_qwen_tongyi')