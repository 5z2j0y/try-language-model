import re
from transformers import AutoTokenizer

# 加载 GPT-2 的 tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# 读取 letter_mt 的 txt
with open("letter_mt.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 按空行分割不同语录
quotes = [quote.strip() for quote in content.split('\n\n') if quote.strip()]

# 处理每条语录：去除中间换行符，过滤token长度
filtered_entries = []
for quote in quotes:
    
    # 计算token数量
    tokens = tokenizer.encode(quote)
    if 50 <= len(tokens) <= 100:
        filtered_entries.append(quote)

# 写入 mark_quotes.txt 文件
with open("mark_quotes.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(filtered_entries))

print(f"✅ 处理完成！最终幽默语录数: {len(filtered_entries)}")