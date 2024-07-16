from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig

tokenizer = AutoTokenizer.from_pretrained("qwen-7b-finetune", trust_remote_code=True)

model = AutoModelForCausalLM.from_pretrained("qwen-7b-finetune", device_map="auto",

trust_remote_code=True).eval()

response, history = model.chat(tokenizer, "", history=None)

print(response)