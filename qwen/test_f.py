import os 
import json
import time

os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  #（保证程序cuda序号与实际cuda序号对应）
os.environ['CUDA_VISIBLE_DEVICES'] = "2"  #（代表仅使用第0，1号GPU）

from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

tokenizer = AutoTokenizer.from_pretrained("qwen-7b-finetune-0806", trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained("qwen-7b-finetune-0806", device_map="auto",

trust_remote_code=True).eval()



def test_acc(test_filename, result_filename):
    f = open(test_filename, encoding='utf_8')
    j_data = json.load(f)
    o_data = []
    time_start = time.time()  # 记录开始时间

    for each in j_data:
        response, history = model.chat(tokenizer, each['conversations'][0]['value'], history=None)
        data ={
            "id": each['id'],
            "conversations": [
                {
                    "from": "user",
                    "value": "{}".format(each['conversations'][0]['value'])
                },
                {
                    "from": "assistant",
                    "value": "{}".format(response)
                }
            ]
        }
        o_data.append(data)
        print(response)
    time_end = time.time()  # 记录结束时间
    time_sum = time_end - time_start  # 计算的时间差为程序的执行时间，单位为秒/s
    print(time_sum)
    print(time_sum / len(j_data))
    f_o = open(result_filename, 'w', encoding='utf_8')
    json.dump(o_data, f_o, ensure_ascii=False, indent=4)
    f_o.close()
    
if __name__ == "__main__":
    test_acc('./bcc_qwen_tongyi/bcc_test.json', './bcc_qwen_tongyi/bcc_test_out.json')
