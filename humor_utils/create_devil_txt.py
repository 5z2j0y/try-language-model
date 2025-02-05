import re
from transformers import AutoTokenizer

# 加载 GPT-2 的 tokenizer
tokenizer = AutoTokenizer.from_pretrained("gpt2")

# 读取 The Devil's Dictionary 的 txt
with open("devils_dictionary.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

entries = []
current_entry = []
capture = False

# 扩展正则匹配：匹配 WORD, n./adj./v.t. 这样的定义
definition_pattern = re.compile(r"^[A-Z][A-Z]+, (n\.|adj\.|v\.t\.)")

for line in lines:
    line = line.strip()
    
    # 如果匹配到新的定义，说明前一个条目结束，存储它
    if definition_pattern.match(line):
        if current_entry:
            entries.append(" ".join(current_entry))
            current_entry = []
        # 开始新的定义
        capture = True
        # 清理掉词条和词性说明
        line = re.sub(r"^[A-Z][A-Z]+, (n\.|adj\.|v\.t\.)\s*", "", line)

    if capture:
        current_entry.append(line)

# 存储最后一个条目
if current_entry:
    entries.append(" ".join(current_entry))

# 修改过滤逻辑，对长文本进行截断
filtered_entries = []
for entry in entries:
    tokens = tokenizer.encode(entry)
    token_length = len(tokens)
    if token_length < 50:
        continue
    
    if token_length > 100:
        # 截断到前100个token并解码回文本
        truncated_tokens = tokens[:100]
        entry = tokenizer.decode(truncated_tokens)
    
    filtered_entries.append(entry)

# 写入 devil_items.txt
with open("devil_items.txt", "w", encoding="utf-8") as f:
    for entry in filtered_entries:
        f.write(entry + "\n")

print(f"✅ 处理完成！最终幽默条目数: {len(filtered_entries)}")