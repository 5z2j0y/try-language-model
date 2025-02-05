import re
from transformers import AutoTokenizer

# 加载 GPT-2 的 tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# 读取 grok_posts 的 txt
with open("grok_posts.txt", "r", encoding="utf-8") as f:
    content = f.read()

# 按空行分割不同语录
quotes = [quote.strip() for quote in content.split('\n') if quote.strip()]

# 处理每条语录：去除中间换行符，过滤token长度
filtered_entries = []
for quote in quotes:
    # 计算token数量
    tokens = tokenizer.encode(quote)
    
    if len(tokens) > 100:
        # 截取前100个token并解码回文本
        truncated_tokens = tokens[:100]
        quote = tokenizer.decode(truncated_tokens)
    
    if len(tokens) >= 40:  # 只需判断最小长度，因为已处理了超长情况
        filtered_entries.append(quote)

# 写入 grok_quotes.txt 文件
with open("grok_quotes.txt", "w", encoding="utf-8") as f:
    f.write('\n'.join(filtered_entries))

print(f"✅ 处理完成！最终幽默语录数: {len(filtered_entries)}")