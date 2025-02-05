from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
import os

# 从环境变量获取 token
hf_token = os.getenv('HF_TOKEN')
if not hf_token:
    raise ValueError("请设置 HF_TOKEN 环境变量")

# 加载 tokenizer 和模型
model_name = "google/gemma-2-2b-it"
tokenizer = AutoTokenizer.from_pretrained(model_name, token=hf_token)
model = AutoModelForCausalLM.from_pretrained(model_name, token=hf_token)

# 使用设备加速（如果有 CUDA 设备的话）
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

# 定义一个示例输入
input_text = "how to bake a cake?"

# 将输入文本编码为模型需要的格式
inputs = tokenizer(input_text, return_tensors="pt").to(device)

# 生成模型输出
with torch.no_grad():
    outputs = model.generate(**inputs, max_length=50, num_return_sequences=1)

# 解码并打印生成的文本
generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
print(generated_text)
