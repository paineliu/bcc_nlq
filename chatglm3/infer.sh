#!/bin/bash
 
# 设置环境变量
export CUDA_VISIBLE_DEVICES=1
# export NCCL_P2P_DISABLE="1"
# export NCCL_IB_DISABLE="1"
 
# 执行 Python 脚本


python inference_hf.py output/sql_merge --prompt "请你作为一个SQL终端，根据下面的数据库描述，只需要返回相应的SQL语句即可。下面是一个任务的指令，请写一个恰当的sql完成任务：\n###指令：\n知识数据库中有图片(picture)表、句子(ju)表、视频(video)表、等级(dengji)表、字(zi)表、音频(audio)表、混淆项(hunxiao)表、词句(ci_ju)表、词图(ci_picture)表、词音(ci_video)表、搭配(ci_dapei)表以及字搭配(zi_dapei)表。\n图片(picture)表有如下列：id, 标签(tags), 意图标签(intention_tags), 路径(url), id是主键。\n句子(ju)表有如下列：id, 句子(ju), md5(md5), 分词序列(ci), 词性标注序列(pos), 长度(len), 平均等级(avg_level), id是主键。\n视频(video)表有如下列：id, 标签(tags), 意图标签(intention_tags), 路径(url), id是主键。\n等级(dengji)表有如下列：id, 内容(term), 类型(type), 识读等级(shidu_level), 书写等级(shuxie_level), id是主键。\n字(zi)表有如下列：id, 字(zi), 识读等级(shidu_level), 书写等级(shuxie_level), id是主键。\n音频(audio)表有如下列：id, 标签(tags), 路径(url), id是主键。\n混淆项(hunxiao)表有如下列：id, 内容(term), 拼音(term_pinyin), 词性(term_pos), 来源(source), 混淆项(hunxiao), 混淆项拼音(hunxiao_pinyin), 混淆项词性(hunxiao_pos), 类型(type), 频次(freq), 主键是id。\n词句(ci_ju)表有如下列：词(ci), 句ID(r_id), ci是主键。\n词图(ci_picture)表有如下列：词(ci), 图ID(r_id), ci是主键。\n词音(ci_video)表有如下列：词(ci), 音频ID(r_id), ci是主键。\n词搭配(ci_dapei)表有如下列：id, 词(ci), 搭配类型(dapei_type), 搭配(dapei), 频次(freq), id为主键。\n字搭配(zi_dapei)表有如下列：id, 字(zi), 词(ci), 词等级(ci_level), 词频(ci_freq), id为主键。\n包含词语\"沿线\"的句子。"
# python inference_hf.py output/cql_merge --prompt "请将下文解析成CQL语句：\n找到形如\"我们 家\"的词语，其中\"家\"是普通名词。"
# python inference_hf.py output/bcc_merge --prompt "请将下文解析成BCC检索式：\n\"王方\"加\"的\"加任意一个或者多个字"