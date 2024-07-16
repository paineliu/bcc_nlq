#!/bin/bash
 
# 设置环境变量
export CUDA_VISIBLE_DEVICES=2
export NCCL_P2P_DISABLE="1"
export NCCL_IB_DISABLE="1"
 
# 执行 Python 脚本


python test_hf.py output/checkpoint-3000 --test-file ./data/sql_test.json --output-file ./data/sql_test_out.json
