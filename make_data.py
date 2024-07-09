import re
import pkuseg
import random

def get_ci_rand_list(ci):
    ci_list = []
    ci_list.append(ci)
    return ci_list

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

def get_sample_pos_limit(tokens, a, b):
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('{}/{}'.format(item[0], item[1]))
        elif (i == b):
            bcc.append('{}/{}'.format(item[0], item[1]))
        else:
            bcc.append(item[0])
    if a == b:
        if a > 0:
            return [' '.join(bcc[a-1: a+1])]
        else:
            return [' '.join(bcc[a: a+2])]
    else:
        return [' '.join(bcc[a: b+1])]
    return [' '.join(bcc)]

def get_sample(tokens, a, b):
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('({})'.format(item[1]))
        elif (i == b):
            bcc.append('({})'.format(item[1]))
        else:
            bcc.append(item[0])
    return [' '.join(bcc)]

def get_sample_len(tokens, a, b):
    bcc_list = []
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('({})'.format(item[1]))
        elif (i == b):
            bcc.append('({})'.format(item[1]))
        else:
            bcc.append(item[0])
    if a == b:
        bcc_len = bcc
        if (tokens[a][1] != 'w'):
            bcc_len.append("{{len($1)={}}}".format(len(tokens[a][0])))
        bcc_list.append(' '.join(bcc_len))
    else:
        bcc_len = bcc
        if (tokens[a][1] == 'w'):
            bcc_len.append("{{len($2)={}}}".format(len(tokens[b][0])))
        elif (tokens[b][1] == 'w'):
            bcc_len.append("{{len($1)={}}}".format(len(tokens[a][0])))
        else:
            bcc_len.append("{{len($1)={};len($2)={}}}".format(len(tokens[a][0]),len(tokens[b][0])))
        bcc_list.append(' '.join(bcc_len))
    return bcc_list

def get_sample_match_len(tokens, a, b):
    bcc_list = []
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('({})'.format(item[1]))
        elif (i == b):
            bcc.append('({})'.format(item[1]))
        else:
            bcc.append(item[0])
    if a == b:
        bcc_len = bcc
        if (tokens[a][1] != 'w'):
            bcc_len.append("{{len($1)={}}}".format(len(tokens[a][0])))
        bcc_list.append(' '.join(bcc_len))
    else:
        bcc_len = bcc
        if (tokens[a][1] == 'w'):
            bcc_len.append("{{len($2)={}}}".format(len(tokens[b][0])))
        elif (tokens[b][1] == 'w'):
            bcc_len.append("{{len($1)={}}}".format(len(tokens[a][0])))
        else:
            bcc_len.append("{{len($1)={};len($2)={}}}".format(len(tokens[a][0]),len(tokens[b][0])))
        bcc_list.append(' '.join(bcc_len))
    return bcc_list

def get_sample_wildcard(tokens, a, b):
    bcc_list = []
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('.' * len(item[0]))
        else:
            bcc.append(item[0])
    bcc_list.append(' '.join(bcc))

    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('.' * len(item[0]) + '/{}'.format(item[1]))
        else:
            bcc.append(item[0])
    bcc_list.append(' '.join(bcc))
    
    bcc = []
    for i, item in enumerate(tokens):
        if (i == a):
            bcc.append('.' * len(item[0]) + '/[{} v]'.format(item[1]))
        else:
            bcc.append(item[0])
    bcc_list.append(' '.join(bcc))

    if (a != b):
        bcc = []
        for i, item in enumerate(tokens):
            if (i == b):
                bcc.append('.' * len(item[0]) + '/{}'.format(item[1]))
            else:
                bcc.append(item[0])
        bcc_list.append(' '.join(bcc))
    return bcc_list

def get_sample_interval(token, a, b):
    pass

def get_sample_collect(token, a, b):
    pass

pku_seg = pkuseg.pkuseg(postag=True)           # 以默认配置加载模型
        
f = open('./data/rmrb/2014-01.txt', encoding='utf_8')
for each in f:
    each = each.strip()
    sentences = re.split(r"([.。!！?？\s+])", each)
    sentences.append("")
    sentences = ["".join(i) for i in zip(sentences[0::2],sentences[1::2])]
    for sen in sentences:
        if len(sen) >=5 and len(sen) <= 15:
            sen = '今天天气很不错！'
            tokens = pku_seg.cut(sen)    # 进行分词和词性标注
            a = random.randint(0, len(tokens) - 1)
            b = a
            if (random.random() < 0.3):
                b = random.randint(0, len(tokens) - 1)
                if a != b:
                    print(a, b)
                else:
                    print(a)
            else:
                print(a)
            if a > b:
                c = b
                b = a
                a = c
            # 词性替换：一个加入词性限定；两个词语加入词性限定（可以是集合），另一个词替换为词性（可以是集合）
            # 词性替换：一个、两个词语为词性，无约束
            # 词性替换：加入约束条件（内容、频次、长度）。
            # 通配符替换：，使用 . .. ~ @
            # 通配符替换：，加入词性限定（可以是集合）
            # 属性约束替换：（内容、词长、频率）
            # 离合符替换：仅保留ab中间替换为*，a前替换为*， b后替换为*
            # 集合数据替换：词列表、词性列表

            # bcc = get_sample(tokens,  a, b)
            print(get_pos_rand_list('a'))
            print(get_pos_rand_list('a'))
            print(get_pos_rand_list('v'))
            print(get_pos_rand_list('v'))
            
            bcc = get_sample_pos_limit(tokens, a, b)
            print(sen, tokens, a, b, bcc)
