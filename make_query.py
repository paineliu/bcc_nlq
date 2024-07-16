import re
import pkuseg
import random
import json
import unicodedata
from random import sample


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
        bcc_limit.append("{{begin(${})=[{}]}}".format(num, ' '.join(get_zi_rand_list(token[0]))))
        bcc_limit.append("{{end(${})=[{}]}}".format(num, ' '.join(get_zi_rand_list(token[-1]))))
        bcc_limit.append("{{begin(${})!=[{}]}}".format(num, ' '.join(get_zi_not_rand_list(token[0]))))
        bcc_limit.append("{{end(${})!=[{}]}}".format(num, ' '.join(get_zi_not_rand_list(token[-1]))))
    if len(token) > 2:
        bcc_limit.append("{{mid(${})=[{}]}}".format(num, ' '.join(get_zi_rand_list(token[1]))))
        bcc_limit.append("{{mid(${})!=[{}]}}".format(num, ' '.join(get_zi_not_rand_list(token[1]))))

def cut_sample(bcc_list, a, b):
    ret_list = []
    for tokens in bcc_list:
        if a == b:
            ret_list.append(' '.join(tokens[max(a - 1, 0): min(a + 2, len(tokens))]))
        else:
            ret_list.append(' '.join(tokens[a: b + 1]))
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

# 生成带词性限制的表达式
def get_sample_pos_limit(tokens, a, b):
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

            bcc_limit.append("{{len($1)={}; len($2)={}}}".format(len(tokens[a][0]),len(tokens[b][0])))
            bcc_limit.append("{{len($1)!={}; len($2)={}}}".format(len(tokens[a][0]) + 1,len(tokens[b][0])))
            bcc_limit.append("{{len($1)={}; len($2)!={}}}".format(len(tokens[a][0]), len(tokens[b][0]) + 1))
            bcc_limit.append("{{len($1)!={}; len($2)!={}}}".format(len(tokens[a][0]) + 1,len(tokens[b][0])+ 1))
            
            if len(tokens[a][0]) > 1 and len(tokens[b][0]) > 1:
                bcc_limit.append("{{len($1)>{}; len($2)={}}}".format(len(tokens[a][0]) - 1, len(tokens[b][0])))
                bcc_limit.append("{{len($1)>{}; len($2)>{}}}".format(len(tokens[a][0]) - 1, len(tokens[b][0]) - 1))
                bcc_limit.append("{{len($1)<{}; len($2)>{}}}".format(len(tokens[a][0]) + 1, len(tokens[b][0]) - 1))
                
                bcc_limit.append("{{begin($1)=[{}]; len($2)={}}}".format(' '.join(get_zi_rand_list(tokens[a][0])), len(tokens[b][0])))
                bcc_limit.append("{{end($1)=[{}]; len($2)={}}}".format(' '.join(get_zi_rand_list(tokens[a][-1])), len(tokens[b][0])))
                bcc_limit.append("{{begin($1)!=[{}]; len($2)>{}}}".format(' '.join(get_zi_not_rand_list(tokens[a][0])), len(tokens[b][0]) - 1))
                bcc_limit.append("{{end($1)!=[{}]; len($2)>{}}}".format(' '.join(get_zi_not_rand_list(tokens[a][-1])), len(tokens[b][0]) - 1))
                
                bcc_limit.append("{{len($1)={}; begin($2)=[{}]}}".format(len(tokens[a][0]), ' '.join(get_zi_rand_list(tokens[b][0]))))
                bcc_limit.append("{{len($1)={}; end($2)=[{}]}}".format(len(tokens[a][0]), ' '.join(get_zi_rand_list(tokens[b][-1]))))
                bcc_limit.append("{{len($1)>{}; begin($2)!=[{}]}}".format(len(tokens[a][0]) - 1, ' '.join(get_zi_not_rand_list(tokens[b][0]))))
                bcc_limit.append("{{len($1)>{}; end($2)!=[{}]}}".format(len(tokens[a][0]) - 1, ' '.join(get_zi_not_rand_list(tokens[b][-1]))))

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

def get_sample(tokens, a, b):
    sample_list = []
    sample_list += get_sample_phrase(tokens, a, b)
    sample_list += get_sample_pos(tokens, a, b)
    sample_list += get_sample_constraint(tokens, a, b)
    sample_list += get_sample_pos_limit(tokens, a, b)
    sample_list += get_sample_wildcard(tokens, a, b)
    return sample_list    

def make_sen_data(data_filenames, sen_filename):

    f_sen = open(sen_filename, 'w', encoding='utf-8')
    for data_filename in data_filenames:
        f = open(data_filename, encoding='utf_8')
        for each in f:
            each = each.strip()
            sentences = re.split(r"([.。!！?？\s+])", each)
            sentences.append("")
            sentences = ["".join(i) for i in zip(sentences[0::2],sentences[1::2])]
            for sen in sentences:
                if len(sen) >=5 and len(sen) <= 15 and not has_number_sen(sen):
                    f_sen.write(sen)
                    f_sen.write('\n')
                    
def make_query_data(sen_filename, query_filename):
    pku_seg = pkuseg.pkuseg(postag=True)
    query_list = []
    f = open(sen_filename, encoding='utf_8')
    for each in f:
        sen = each.strip()
        tokens = pku_seg.cut(sen)    # 进行分词和词性标注
        a = random.randint(0, len(tokens) - 1)
        b = a

        if (random.random() < 0.3):
            b = random.randint(0, len(tokens) - 1)
        if a > b:
            c = b
            b = a
            a = c         
        sample_list = get_sample(tokens, a, b)
        query_list.append({'query':sample(sample_list, 1)[0], 'sentence':sen})
        print(len(query_list))

    f = open(query_filename, 'w', encoding='utf_8')
    json.dump(query_list, f, ensure_ascii=False, indent=4)
    f.close()

if __name__ == '__main__':

    make_sen_data(['./data/rmrb/2015-01.txt', './data/rmrb/2015-12.txt'], './data/rmrb_data.txt')
    make_query_data('./data/rmrb_data.txt', './data/rmrb_query.json')
