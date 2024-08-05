import re
import pkuseg
import random
import json
import unicodedata
from random import sample
import pandas as pd


def is_number(char):
    if char.isdigit():
        return True
    else:
        return False

def has_number_sen(sentence):
    for char in sentence:
        if is_number(char):
            return True
    return False

def is_chinese(char):
    if 'CJK' in unicodedata.name(char):
        return True
    else:
        return False

def is_chinese_sen(word):
    for char in word:
        if not is_chinese(char):
            return False
    return True

def add_limit_list(token, num, bcc_limit):
    bcc_limit.append("{{len(${})={}}}".format(num, len(token)))
    bcc_limit.append("{{len(${})!={}}}".format(num, len(token) + 1))
    if len(token) > 1:
        bcc_limit.append("{{len(${})>{}}}".format(num, len(token) - 1))
        bcc_limit.append("{{len(${})<{}}}".format(num, len(token) + 1))
        bcc_limit.append("{{begin(${})=[{}]}}".format(num, '+'.join(get_zi_rand_list(token[0]))))
        bcc_limit.append("{{end(${})=[{}]}}".format(num, '+'.join(get_zi_rand_list(token[-1]))))
        bcc_limit.append("{{begin(${})!=[{}]}}".format(num, '+'.join(get_zi_not_rand_list(token[0]))))
        bcc_limit.append("{{end(${})!=[{}]}}".format(num, '+'.join(get_zi_not_rand_list(token[-1]))))
    if len(token) > 2:
        bcc_limit.append("{{mid(${})=[{}]}}".format(num, '+'.join(get_zi_rand_list(token[1]))))
        bcc_limit.append("{{mid(${})!=[{}]}}".format(num, '+'.join(get_zi_not_rand_list(token[1]))))

def cut_sample(bcc_list, a, b):
    ret_list = []
    for tokens in bcc_list:
        if a == b:
            ret_list.append('+'.join(tokens[max(a - 1, 0): min(a + 2, len(tokens))]))
        else:
            ret_list.append('+'.join(tokens[a: b + 1]))
    return ret_list

def get_ci_rand_list(ci):
    ci_data = []
    f = open('./data/phrase.txt', encoding='utf-8')
    for each in f:
        items = each.split()
        if is_chinese_sen(items[0]):
            ci_data.append(items[0])
            if len(ci_data) >= 1000:
                break
            
    ci_list = []
    ci_list.append(ci)
    total = random.randint(2, 4)
    for i in range(100):
        t = random.choice(ci_data)
        if t not in ci_list:
            ci_list.append(t)
        if len(ci_list) >= total:
            break

    return ci_list

def get_zi_rand_list(zi):
    zi_data = []
    f = open('./data/phrase.txt', encoding='utf-8')
    for each in f:
        items = each.split()
        if len(items[0]) == 1 and is_chinese_sen(items[0]):
            zi_data.append(items[0])
            if len(zi_data) >= 1000:
                break
            
    zi_list = []
    zi_list.append(zi)
    total = random.randint(2, 4)
    for i in range(100):
        t = random.choice(zi_data)
        if t not in zi_list:
            zi_list.append(t)
        if len(zi_list) >= total:
            break

    return zi_list

def get_zi_not_rand_list(zi):
    zi_data = []
    f = open('./data/phrase.txt', encoding='utf-8')
    for each in f:
        items = each.split()
        if len(items[0]) == 1 and is_chinese_sen(items[0]):
            zi_data.append(items[0])
            if len(zi_data) >= 1000:
                break
            
    zi_list = []
    total = random.randint(2, 4)
    for i in range(100):
        t = random.choice(zi_data)
        if t != zi and t not in zi_list:
            zi_list.append(t)
        if len(zi_list) >= total:
            break

    return zi_list

def get_pos_rand_list(pos):
    pos_data = ['Ag','i','o','vn','a','j','p','w','ad','k','q','x','an','l','r','y','b','m','s','z','c','Ng','Tg','un','Dg','n','t','h','d','nr','u','g','e','ns','Vg','nz','f','nt','v','vd']
    
    pos_list = []
    pos_list.append(pos)
    total = random.randint(2, 4)
    for i in range(100):
        t = random.choice(pos_data)
        if t not in pos_list:
            pos_list.append(t)
        if len(pos_list) >= total:
            break

    return pos_list
    
# 生成简单的查询词
def get_sample_phrase(tokens, a, b):
    bcc_list = []
    bcc_list.append(tokens[a][0])
    if a != b:
        bcc_list.append(tokens[b][0])

    return bcc_list

# 生成带范围限制的表达式
def get_sample_range(tokens, a, b):
    bcc_list = []
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('[{}]'.format('+'.join(get_ci_rand_list(item[0]))))
        elif (i == b):
            bcc.append('[{}]'.format('+'.join(get_ci_rand_list(item[0]))))
        else:
            bcc.append(item[0])
    bcc_list.append(bcc)
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('[{}]'.format('+'.join(get_pos_rand_list(item[1]))))
        elif (i == b):
            bcc.append('[{}]'.format('+'.join(get_pos_rand_list(item[1]))))
        else:
            bcc.append(item[0])
    bcc_list.append(bcc)
    return cut_sample(bcc_list, a, b)

# 生成带词性限制的表达式
def get_sample_limit(tokens, a, b):
    bcc_list = []
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('{}/{}'.format(item[0], item[1]))
        elif (i == b):
            bcc.append('{}/{}'.format(item[0], item[1]))
        else:
            bcc.append(item[0])
    bcc_list.append(bcc)
    return cut_sample(bcc_list, a, b)

# 将词语替换为词性
def get_sample_pos(tokens, a, b):
    bcc_list = []
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('{}'.format(item[1]))
        elif (i == b):
            bcc.append('{}'.format(item[1]))
        else:
            bcc.append(item[0])
    bcc_list.append(bcc)
    return cut_sample(bcc_list, a, b)

# 将词语替换为词性，再加入限定条件
def get_sample_constraint(tokens, a, b):
    bcc_list = []
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('({})'.format(item[1]))
        elif (i == b):
            bcc.append('({})'.format(item[1]))
        else:
            bcc.append(item[0])
    bcc_list.append(bcc)

    bcc_limit = []
    bcc_limit.append("{{count>{}}}".format(random.randint(2, 10)))
    bcc_limit.append("{{count<{}}}".format(random.randint(100, 1000)))
    
    if a == b:
        if (tokens[a][1] != 'w'):
            add_limit_list(tokens[a][0], 1, bcc_limit)
    else:
        bcc_limit.append("{$1=$2}")
        bcc_limit.append("{$1!=$2}")

        if (tokens[a][1] == 'w'):
            add_limit_list(tokens[b][0], 2, bcc_limit)
        elif (tokens[b][1] == 'w'):
            add_limit_list(tokens[a][0], 1, bcc_limit)
        else:
            add_limit_list(tokens[a][0], 1, bcc_limit)
            add_limit_list(tokens[b][0], 2, bcc_limit)

            bcc_limit.append("{{len($1)={}; len($2)={}}}".format(len(tokens[a][0]), len(tokens[b][0])))
            bcc_limit.append("{{len($1)!={}; len($2)={}}}".format(len(tokens[a][0]) + 1, len(tokens[b][0])))
            bcc_limit.append("{{len($1)={}; len($2)!={}}}".format(len(tokens[a][0]), len(tokens[b][0]) + 1))
            bcc_limit.append("{{len($1)!={}; len($2)!={}}}".format(len(tokens[a][0]) + 1,len(tokens[b][0])+ 1))
            
            if len(tokens[a][0]) > 1 and len(tokens[b][0]) > 1:
                bcc_limit.append("{{len($1)>{}; len($2)={}}}".format(len(tokens[a][0]) - 1, len(tokens[b][0])))
                bcc_limit.append("{{len($1)>{}; len($2)>{}}}".format(len(tokens[a][0]) - 1, len(tokens[b][0]) - 1))
                bcc_limit.append("{{len($1)<{}; len($2)>{}}}".format(len(tokens[a][0]) + 1, len(tokens[b][0]) - 1))
                
                bcc_limit.append("{{begin($1)=[{}]; len($2)={}}}".format('+'.join(get_zi_rand_list(tokens[a][0])), len(tokens[b][0])))
                bcc_limit.append("{{end($1)=[{}]; len($2)={}}}".format('+'.join(get_zi_rand_list(tokens[a][-1])), len(tokens[b][0])))
                bcc_limit.append("{{begin($1)!=[{}]; len($2)>{}}}".format('+'.join(get_zi_not_rand_list(tokens[a][0])), len(tokens[b][0]) - 1))
                bcc_limit.append("{{end($1)!=[{}]; len($2)>{}}}".format('+'.join(get_zi_not_rand_list(tokens[a][-1])), len(tokens[b][0]) - 1))
                
                bcc_limit.append("{{len($1)={}; begin($2)=[{}]}}".format(len(tokens[a][0]), '+'.join(get_zi_rand_list(tokens[b][0]))))
                bcc_limit.append("{{len($1)={}; end($2)=[{}]}}".format(len(tokens[a][0]), '+'.join(get_zi_rand_list(tokens[b][-1]))))
                bcc_limit.append("{{len($1)>{}; begin($2)!=[{}]}}".format(len(tokens[a][0]) - 1, '+'.join(get_zi_not_rand_list(tokens[b][0]))))
                bcc_limit.append("{{len($1)>{}; end($2)!=[{}]}}".format(len(tokens[a][0]) - 1, '+'.join(get_zi_not_rand_list(tokens[b][-1]))))

    bcc_list = cut_sample(bcc_list, a, b)
    bcc_result = []
    for bcc in bcc_list:
        for limit in bcc_limit:
            bcc_data = '{}{}'.format(bcc, limit)
            bcc_result.append(bcc_data)

    return bcc_result

# 处理通配符
def get_sample_wildcard(tokens, a, b):
    bcc_list = []
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('.' * len(item[0]))
        else:
            bcc.append(item[0])
    bcc_list.append(cut_sample([bcc], a, a)[0])

    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('.' * len(item[0]) + '/{}'.format(item[1]))
        else:
            bcc.append(item[0])
    bcc_list.append(cut_sample([bcc], a, a)[0])

    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('.' * len(item[0]) + '/[{} v]'.format(item[1]))
        else:
            bcc.append(item[0])
    bcc_list.append(cut_sample([bcc], a, a)[0])

    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('~')
        else:
            bcc.append(item[0])
    bcc_list.append(cut_sample([bcc], a, a)[0])

    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('~' + '/[{} v]'.format(item[1]))
        else:
            bcc.append(item[0])
    bcc_list.append(cut_sample([bcc], a, a)[0])

    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('@')
        else:
            bcc.append(item[0])
    bcc_list.append(cut_sample([bcc], a, a)[0])

    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('@' + '/[{} v]'.format(item[1]))
        else:
            bcc.append(item[0])
    bcc_list.append(cut_sample([bcc], a, a)[0])

    if (a + 1 < b):
        bcc = []
        for i, item in enumerate(tokens):
            if (i == a):
                bcc.append('.' * len(item[0]) + '/{}'.format(item[1]))
            elif (i == b):
                bcc.append('.' * len(item[0]) + '/{}'.format(item[1]))
            else:
                bcc.append(item[0])
        bcc_list.append(cut_sample([bcc], a, b)[0])
        bcc = []
        for i, item in enumerate(tokens):
            if (i == a):
                bcc.append('.' * len(item[0]))
            elif (i == b):
                bcc.append('.' * len(item[0]))
            else:
                bcc.append(item[0])
        bcc_list.append(cut_sample([bcc], a, b)[0])

    return bcc_list

def get_sample_by_tokens(tokens, a, b, types):
    sample_list = []
    if 1 in types:
        sample_list += get_sample_phrase(tokens, a, b)
    if 2 in types:
        sample_list += get_sample_pos(tokens, a, b)
    if 3 in types:
        sample_list += get_sample_wildcard(tokens, a, b)
    if 4 in types:
        sample_list += get_sample_range(tokens, a, b)
    if 5 in types:
        sample_list += get_sample_limit(tokens, a, b)
    if 6 in types:
        sample_list += get_sample_constraint(tokens, a, b)
    return sample_list    

def get_sample_by_sentence(pku_seg, sen, types):
    tokens = pku_seg.cut(sen)    # 进行分词和词性标注
    a = random.randint(0, len(tokens) - 1)
    b = a

    if (random.random() < 0.3):
        b = random.randint(0, len(tokens) - 1)
    if a > b:
        c = b
        b = a
        a = c         

    sample_list = get_sample_by_tokens(tokens, a, b, types)
    return sample_list
    
def make_sen_data(data_filenames, sen_filename):

    sen_set = set()
    f_sen = open(sen_filename, 'w', encoding='utf-8')
    for data_filename in data_filenames:
        f = open(data_filename, encoding='utf_8')
        for each in f:
            each = each.strip()
            sentences = re.split(r"([.。!！?？\s+])", each)
            sentences.append("")
            sentences = ["".join(i) for i in zip(sentences[0::2],sentences[1::2])]
            for sen in sentences:
                if len(sen) >=5 and len(sen) <= 15 and not has_number_sen(sen) and sen not in sen_set:
                    sen_set.add(sen)
                    f_sen.write(sen)
                    f_sen.write('\n')
                    

def load_log_data(log_filename):
    df = pd.read_csv(log_filename)
    map_log_data = {}
    for i in range(1, 9):
        map_log_data[i] = set()

    for i in range(len(df)):
        query = df['query'][i]
        type = df['type'][i]
        if type == 1:
            map_log_data[1].add(query)
        elif type == 2:
            map_log_data[2].add(query)
        elif type == 3:
            map_log_data[5].add(query)
        elif type == 4:
            map_log_data[4].add(query)
        elif type == 5:
            map_log_data[6].add(query)
        elif type >= 6 and type <= 10:
            map_log_data[3].add(query)
        elif type >= 11 and type <= 12:
            map_log_data[7].add(query)
        else:
            map_log_data[8].add(query)
    return map_log_data

def gen_sample(pku_seg, sen_filename, type, set_query, gen_total):
    f = open(sen_filename, encoding='utf_8')
    sens = f.readlines()
    while len(set_query) < gen_total:
        sen = sample(sens, 1)[0]
        sen = sen.strip()
        sample_list = get_sample_by_sentence(pku_seg, sen, [type])
        query = sample(sample_list, 1)[0]
        if (query not in set_query):
            set_query.add(query)

def make_query_data(log_filename, sen_filename, query_filename):
    print(query_filename)
    pku_seg = pkuseg.pkuseg(postag=True)
    sample_rate = [0, 2, 2, 1, 2, 1, 1]
    map_log_data = load_log_data(log_filename)
    for i in range(1, 7):
        gen_total = 2000 * sample_rate[i]
        gen_sample(pku_seg, sen_filename, i, map_log_data[i], gen_total)

    f = open(query_filename, 'w', encoding='utf_8_sig')
    f.write("{},{}\n".format('query', 'type'))
    for i in range(1, 7):
        out_item = 0
        for query in  map_log_data[i]:
            out_item += 1
            f.write("{},{}\n".format(query, i))
            if '+' in query:
                query2 = query.replace('+', ' ')
                f.write("{},{}\n".format(query2, i))
            
            if out_item >= sample_rate[i] * 2000:
                break 
    f.close()

def get_error_by_sentence(pku_seg, sen):

    tokens = pku_seg.cut(sen)    # 进行分词和词性标注
    a = random.randint(0, len(tokens) - 1)
    b = a

    if (random.random() < 0.3):
        b = random.randint(0, len(tokens) - 1)
    if a > b:
        c = b
        b = a
        a = c         

    sample_map = {}
    if a == b:
        # 要是{len(30}
        sample_map['{}{{len({})}}'.format(tokens[a][0], len(tokens[a][0]))] = '语法错误，限制条件格式错误'

        # (v)着{($1)>1}
        rand_ci = sample(get_ci_rand_list("着"), 1)[0]
        sample_map['({}){}{{($1)>{}}}'.format(tokens[a][1], rand_ci, len(tokens[a][0]))] = '({}){}{{len($1)>{}}}'.format(tokens[a][1], rand_ci, len(tokens[a][0]))
        sample_map['({}){}{{($1)={}}}'.format(tokens[a][1], rand_ci, len(tokens[a][0]))] = '({}){}{{len($1)={}}}'.format(tokens[a][1], rand_ci, len(tokens[a][0]))
        sample_map['({}){}{{($1)<{}}}'.format(tokens[a][1], rand_ci, len(tokens[a][0]) + 1)] = '({}){}{{len($1)<{}}}'.format(tokens[a][1], rand_ci, len(tokens[a][0]) + 1)
        
    else:
        # 通配符重复 诞辰****周年
        sample_map['{}{}{}'.format(tokens[a][0], '*' * (1 + len(tokens[a][0])), tokens[b][0])] = '{}{}{}'.format(tokens[a][0], '*', tokens[b][0])
        sample_map['{}{}'.format('*' * (1 + len(tokens[a][0])), tokens[b][0])] = '{}{}'.format('*', tokens[b][0])
        sample_map['{}{}'.format('*' * (1 + len(tokens[a][0])), tokens[b][0])] = '{}{}'.format('*', tokens[b][0])

        sample_map['{}{}{}'.format(tokens[a][0], '@' * (1 + len(tokens[a][0])), tokens[b][0])] = '{}{}{}'.format(tokens[a][0], '@', tokens[b][0])
        sample_map['{}{}{}'.format(tokens[a][0], '@' * (1 + len(tokens[a][0])), tokens[b][0])] = '{}{}{}'.format(tokens[a][0], '@', tokens[b][0])

        # 没n就v{$1=$2}
        rand_pos1= sample(get_pos_rand_list('n'), 1)[0]
        rand_pos2= sample(get_pos_rand_list('v'), 1)[0]
        sample_map['{}{}{}{}{{$1=$2}}'.format(tokens[a][0], rand_pos1, tokens[b][0], rand_pos2)] = '{}({}){}({}){{$1=$2}}'.format(tokens[a][0], rand_pos1, tokens[b][0], rand_pos2)
        sample_map['{}{}{{len($1)={}}}'.format(tokens[a][0], rand_pos1, len(tokens[a][0]))] = '{}({}){{len($1)={}}}'.format(tokens[a][0], rand_pos1, len(tokens[a][0]))
        sample_map['{}{}{{len($1)>{}}}'.format(rand_pos2, tokens[b][0], len(tokens[b][0]))] = '({}){}{{len($1)>{}}}'.format(rand_pos2, tokens[b][0], len(tokens[b][0]))
    # for each in sample_map:
    #     print(each, sample_map[each])
    return sample_map

def pick_random_key(dictionary):
    keys = list(dictionary.keys())
    if not keys:
        return None
    return random.choice(keys)

def gen_error(pku_seg, sen_filename, map_query, gen_total):
    f = open(sen_filename, encoding='utf_8')
    sens = f.readlines()
    while len(map_query) < gen_total:
        sen = sample(sens, 1)[0]
        sen = sen.strip()
        sample_map = get_error_by_sentence(pku_seg, sen)
        random_key = pick_random_key(sample_map)
        # print(random_key, sample_map[random_key])
        map_query[random_key] = sample_map[random_key]

def make_error_data(log_filename, sen_filename, query_filename):
    print(query_filename)
    pku_seg = pkuseg.pkuseg(postag=True)
    sample_rate = [0, 0, 0, 0, 0, 0, 0, 1, 1]
    set_log_data = load_log_data(log_filename)
    map_log_data = {}
    map_fix_data = {}
    out_item = 0
    for item in set_log_data[7]:
        out_item += 1
        if '^' in item:
            map_log_data[item] = '语法错误，存在无效符号“^”'
        elif '-' in item:
            map_log_data[item] = '语法错误，存在无效符号“-”'
        if len(map_log_data) >= 1000:
            break
    for item in set_log_data[8]:
        if '**女' in item:
            map_fix_data[item] = '*女'
        if '(v)着{($1)>1}' in item:
            map_fix_data[item] = '(v)着{len($1)>1}'
        if '要是{len(30}' in item:
            map_fix_data[item] = '语法错误，限制条件格式错误'

    gen_error(pku_seg, sen_filename, map_fix_data, 1000)


    f = open(query_filename, 'w', encoding='utf_8_sig')
    f.write("{},{},{}\n".format('query', 'respond', 'type'))
    
    for query in  map_log_data:
        f.write("{},{},{}\n".format(query, map_log_data[query], 7))
        if '+' in query:
            query2 = query.replace('+', ' ')
            respond2 = map_log_data[query].replace('+', ' ')
            f.write("{},{},{}\n".format(query2, respond2, 7))
    for query in  map_fix_data:
        f.write("{},{},{}\n".format(query, map_fix_data[query], 8))
        if '+' in query:
            query2 = query.replace('+', ' ')
            respond2 = map_fix_data[query].replace('+', ' ')
            f.write("{},{},{}\n".format(query2, respond2, 7))

    f.close() 

if __name__ == '__main__':

    make_query_data('./data/bcc_log.csv', './data/sentence_data.txt', './data/bcc_query.csv')
    
    make_error_data('./data/bcc_log.csv', './data/sentence_data.txt', './data/bcc_fixed.csv')

