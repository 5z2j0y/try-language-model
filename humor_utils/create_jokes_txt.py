from datasets import load_dataset
from transformers import GPT2Tokenizer
from tqdm import tqdm

# 初始化GPT2分词器
tokenizer = GPT2Tokenizer.from_pretrained('gpt2')

# 加载数据集
dataset = load_dataset("ysharma/short_jokes", split="train")
jokes = dataset['Joke']

# 筛选符合长度的笑话
selected_jokes = []
for joke in tqdm(jokes, desc="Processing jokes"):
    tokens = tokenizer.encode(joke)
    if 50 <= len(tokens) <= 100:
        selected_jokes.append(joke)

# 写入文件
print(f"Selected {len(selected_jokes)} jokes")
with open('humor.txt', 'w', encoding='utf-8') as f:
    for joke in selected_jokes:
        f.write(joke.strip() + '\n')