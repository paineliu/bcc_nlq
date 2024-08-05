#!/bin/bash
 
# 设置环境变量
export CUDA_VISIBLE_DEVICES=3
export NCCL_P2P_DISABLE="1"
export NCCL_IB_DISABLE="1"
 
# 执行 Python 脚本


python test_hf.py output/checkpoint-200000 --test-file ./dataset_glm_tongyi/bcc_test_case.json --output-file ./dataset_glm_tongyi/bcc_test_case_out.json
