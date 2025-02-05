import re
from transformers import AutoTokenizer

# 加载 GPT-2 的 tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# 读取 Wilde_quotes 的 txt
with open("Wilde_quotes.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 按空行分割不同语录
quotes = [quote.strip() for quote in content.split('\n\n') if quote.strip()]

# 处理每条语录：去除中间换行符，过滤token长度
filtered_entries = []
for quote in quotes:
    # 将中间的换行符替换为空格
    clean_quote = ' '.join(quote.split('\n'))
    
    # 计算token数量
    tokens = tokenizer.encode(clean_quote)
    if 50 <= len(tokens) <= 100:
        filtered_entries.append(clean_quote)

# 写入 wilde_quotes.txt 文件
with open("wilde_quotes.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(filtered_entries))

print(f"✅ 处理完成！最终幽默语录数: {len(filtered_entries)}")