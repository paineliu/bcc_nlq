import os
import json

def conv_log_cvs(log_filename, loss_filename, rate_filename):
    
    os.makedirs(os.path.dirname(loss_filename), exist_ok=True)

    f_loss = open(loss_filename, 'w', encoding="utf-8")
    f_rate = open(rate_filename, 'w', encoding="utf-8")
    f_loss.write("{},{}\n".format('epoch', 'loss'))
    f_rate.write("{},{}\n".format('epoch', 'learning_rate'))

    f = open(log_filename, encoding="utf-8")
    for each in f:
        each = each.strip()
        if "{'loss':" in each:
            data = each[1:-1]
            items = data.split(",")
            data_map = {}
            for item in items:
                kv = item.split(':')
                key = kv[0].strip()[1:-1]
                val = float(kv[1].strip())
                data_map[key] = val

            f_loss.write("{},{}\n".format(data_map['epoch'], data_map['loss']))
            f_rate.write("{},{}\n".format(data_map['epoch'], data_map['learning_rate']))
    f_loss.close()


if __name__ == '__main__':
    conv_log_cvs('./chatglm3/chatglm3_log_0806.txt', './data/chatglm3_loss.csv', './data/chatglm3_rate.csv')
    # conv_log_cvs('./log/qwen_log.txt', './data/qwen_loss.csv', './data/qwen_rate.csv')