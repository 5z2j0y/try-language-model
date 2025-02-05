import json
from datasets import load_dataset
import random
import matplotlib.pyplot as plt
import numpy as np
from transformers import AutoTokenizer

# 加载GPT-2英文分词器
tokenizer = AutoTokenizer.from_pretrained("gpt2")

def sample_data(dataset, balanced_data_num, output_tokens_num):
    sampled_data = []
    dataset_list = list(dataset)  # 转换为列表便于随机抽样
    
    # 随机抽取指定数量的数据
    sampled_items = random.sample(dataset_list, min(balanced_data_num, len(dataset_list)))
    
    for item in sampled_items:
        joke = item["title"] if item["body"] == "" else item["body"]
        
        # 使用GPT-2分词器计算token数量
        tokenized_output = tokenizer(joke, return_tensors="pt")
        output_tokens_len = len(tokenized_output["input_ids"][0])
        
        # 仅保留长度接近指定output_tokens_num的数据
        if abs(output_tokens_len - output_tokens_num) <= 10:  # 设置一个容差范围
            sampled_data.append({
                "system": "You are a witty AI assistant who always responds humorously.",
                "instruction": item['title'],
                "input": "",
                "output": joke
            })

    return sampled_data

# 加载数据集
dataset = load_dataset("kuldin/english_jokes", split="train")
# 抽取20k数据
balanced_data_num = 190000  # 设置需要采样的数据量
output_tokens_num = 50  # 设置期望的output tokens数量

formatted_data = sample_data(dataset, balanced_data_num, output_tokens_num)
with open("jokes_conversation.json", "w") as f:
    json.dump(formatted_data, f, indent=4)

print(f"\n转换完成，已处理 {len(formatted_data)} 条数据")
print("数据已保存为 jokes_conversation.json")
