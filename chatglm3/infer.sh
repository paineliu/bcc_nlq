#!/bin/bash
 
# 设置环境变量
export CUDA_VISIBLE_DEVICES=3
# export NCCL_P2P_DISABLE="1"
# export NCCL_IB_DISABLE="1"
 
# 执行 Python 脚本
python inference_hf.py output/checkpoint-200000 --prompt "请将下文解析成BCC检索式：\n不如后面接一个词"
