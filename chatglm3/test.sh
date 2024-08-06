#!/bin/bash
 
# 设置环境变量
export CUDA_VISIBLE_DEVICES=3
export NCCL_P2P_DISABLE="1"
export NCCL_IB_DISABLE="1"
 
# 执行 Python 脚本


python test_hf.py output-0806/checkpoint-100000 --test-file ./bcc_glm_tongyi/bcc_test.json --output-file ./bcc_glm_tongyi/bcc_test_out.json
