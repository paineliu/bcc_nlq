import os 
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"  #（保证程序cuda序号与实际cuda序号对应）
os.environ['CUDA_VISIBLE_DEVICES'] = "2"  #（代表仅使用第0，1号GPU）

from peft import AutoPeftModelForCausalLM

from transformers import AutoTokenizer

model = AutoPeftModelForCausalLM.from_pretrained( "./qwen/output_qwen/checkpoint-4000", device_map="auto", trust_remote_code=True ).eval()

merged_model = model.merge_and_unload()

# merged_model.save_pretrained("./qwen-7b-finetune", max_shard_size="2048MB", safe_serialization=True) # 最大分片2g

merged_model.save_pretrained("./qwen-7b-finetune", safe_serialization=True) # 最大分片2g

tokenizer = AutoTokenizer.from_pretrained( "/home/liutingchao/.cache/modelscope/hub/Qwen/Qwen-7B-Chat", trust_remote_code=True )

tokenizer.save_pretrained("./qwen-7b-finetune")