import os
import json
import datetime
import unicodedata

def is_chinese(char):

    if char in [':', "'", '＂', '～', '=', '!', ';', '〇', '‘', '|', '’', '\\', '"', ' ', '【', '%', '（', '）', '￥', '·', '〈', '〉', '“','”', '…', '—', '?', '^', '《', '》', '(', ')', '^', '-', '+', '，', '。', '？', '！', '、', '：', '；'] or char.isdigit() or 'CJK' in unicodedata.name(char):
        return True
    else:
        return False

def is_chinese_query(query):
    for char in query:
        if not is_chinese(char):
            return False
    return True

def is_pos_chinese_query(query):
    for char in query:
        if not is_chinese(char) and not char.isalpha():
            return False
    return True

def is_star_pos_chinese_query(query):
    for char in query:
        if not is_chinese(char) and not char.isalpha() and char not in ['*']:
            return False
    return True

def is_period_pos_chinese_query(query):
    for char in query:
        if not is_chinese(char) and not char.isalpha() and char not in ['.']:
            return False
    return True

def is_tilde_pos_chinese_query(query):
    for char in query:
        if not is_chinese(char) and not char.isalpha() and char not in ['~']:
            return False
    return True

def is_at_pos_chinese_query(query):
    for char in query:
        if not is_chinese(char) and not char.isalpha() and char not in ['@']:
            return False
    return True

def is_wild_pos_chinese_query(query):
    for char in query:
        if not is_chinese(char) and not char.isalpha() and char not in ['@', '~', '.', '*']:
            return False
    return True


def is_condition_query(query):
    if '{' in query:
        return True
    return False


def is_range_query(query):
    if '[' in query:
        return True
    return False

def is_limit_query(query):
    if '/' in query:
        return True
    return False

def get_error_query_type(query):
    for i, s in enumerate(['-', '^', '**', 'len(30', '{(']):
        if s in query:
            return i + 1
    return 0

def get_query_type(query):
    
    err_type = get_error_query_type(query)
    if err_type != 0:
        return 10 + err_type
    
    if is_condition_query(query): # 包含约束条件
        return 5
    if is_range_query(query): # 包含范围条件
        return 4
    if is_limit_query(query): # 包含限定条件
        return 3
    
    if is_chinese_query(query): # 中文串
        return 1
    if is_pos_chinese_query(query): # 词性+中文
        return 2
    
    if is_star_pos_chinese_query(query): # 词性+中文+*
        return 6
    if is_period_pos_chinese_query(query): # 词性+中文+.
        return 7
    if is_tilde_pos_chinese_query(query): # 词性+中文+~
        return 8
    if is_at_pos_chinese_query(query): # 词性+中文+@
        return 9
    if is_wild_pos_chinese_query(query): # 词性+中文+多种通配
        return 10
    return 0

def get_query_type6(query):
    err_type = get_error_query_type(query)
    if err_type != 0:
        return 0
    
    if is_condition_query(query): # 包含约束条件
        return 5
    if is_range_query(query): # 包含范围条件
        return 4
    if is_limit_query(query): # 包含限定条件
        return 3
    
    if is_chinese_query(query): # 中文串
        return 1
    if is_pos_chinese_query(query): # 词性+中文
        return 2
    
    if is_star_pos_chinese_query(query): # 词性+中文+*
        return 6
    if is_period_pos_chinese_query(query): # 词性+中文+.
        return 6
    if is_tilde_pos_chinese_query(query): # 词性+中文+~
        return 6
    if is_at_pos_chinese_query(query): # 词性+中文+@
        return 6
    if is_wild_pos_chinese_query(query): # 词性+中文+多种通配
        return 6
    return 0

def conv_log_cvs(sql_filename, query_filename):
    
    # os.makedirs(os.path.dirname(loss_filename), exist_ok=True)

    f_query = open(query_filename, 'w', encoding="utf_8_sig")
    # f_rate = open(rate_filename, 'w', encoding="utf-8")
    f_query.write("{},{},{},{}\n".format('id', 'corpus', 'query', 'type'))
    # f_rate.write("{},{}\n".format('epoch', 'learning_rate'))
    # id                     记录ID 
    # cid                   语料库ID 
        # '0' => '多领域',
        # '1' => '文学',
        # '2' => '报刊',
        # '3' => '对话',
        # '4' => '篇章检索',
        # '5' => '古汉语',
        # '6' => '树库',
        # '7' => '自定义',

        # '10' => '华尔街日报',
        # '11' => '英语树库',

        # '20' => '英=>汉',
        # '21' => '汉=>英',
        # '22' => '英=>日',
        # '23' => '日=>英',  
        # '24' => '英=>波斯',
        # '25' => '波斯=>英', 
        # '26' => '英=>德',
        # '27' => '德=>英', 
        # '28' => '汉=>土耳其',
        # '29' => '土耳其=>汉',  
    # tid                    操作类型        types = ['0:单语查询', '1:双语查询', '2:词频', '3:出处', '4:显示树', '5:下载', '6:下载词频']
    # input                输入 
    # page                页码 
    # uid                   用户ID (1为游客)
    # update_at        查询时间
    # ip                     IP地址
    uids = set()
    datas = []
    map_cid = {}
    map_type = {}
    
    f = open(sql_filename, encoding="utf_8")
    for each in f:
        each = each.strip()
        if "INSERT INTO `logs`" in each:
            items = each[:-2].split(',')
            query = items[3].strip()[1:-1].strip()
            dt_str = items[8].strip()[1:-1]
            try:
                dt_opt = datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
                dt_begin = datetime.datetime.strptime('2019-12-21 00:00:00', "%Y-%m-%d %H:%M:%S")
                duration = dt_opt - dt_begin
                

                cid = int(items[1].strip())
                tid = int(items[2].strip())
                day = dt_str.split(' ')[0]
                uid = '{} {} {}'.format(day, cid, query)
                if cid < 7 and uid not in uids and query not in ['vÒ±', 'Ò¸v', 'Ò¸', 'Ä¿']:
                    map_cid[cid] = map_cid.get(cid, 0) + 1
                    typeid = get_query_type(query)
                    map_type[typeid] = map_type.get(typeid, 0) + 1
                    uids.add(uid)
                    data_map = {}
                    data_map['cid'] = cid
                    # data_map['tid'] = tid
                    while(query[0] == '+'):
                        query = query[1:]
                    data_map['query'] = query
                    data_map['day'] = duration.days
                    f_query.write("{},{},{},{}\n".format(duration.days, cid, query, typeid))
                    datas.append(data_map)
                    if len(datas) == 70000:
                        break
            except:
                print(each)
    print(len(datas))
    print(map_cid)
    for each in map_cid:
        print(each, map_cid[each])
    print(map_type)
    for each in map_type:
        print(each, map_type[each])
    

if __name__ == '__main__':
    conv_log_cvs('./data/logs.sql', './data/bcc_log.csv')
    