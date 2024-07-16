from peft import AutoPeftModelForCausalLM

from transformers import AutoTokenizer

model = AutoPeftModelForCausalLM.from_pretrained( "qwen/output_qwen", device_map="auto", trust_remote_code=True ).eval()

merged_model = model.merge_and_unload()

merged_model.save_pretrained("qwen-7b-finetune", max_shard_size="2048MB", safe_serialization=True) # 最大分片2g

tokenizer = AutoTokenizer.from_pretrained( "output_qwen", trust_remote_code=True )

tokenizer.save_pretrained("qwen-7b-finetune")