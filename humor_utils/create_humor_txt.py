import os
import random
from collections import defaultdict
from pathlib import Path

def merge_and_shuffle_txt():
    # 获取所有txt文件路径
    data_dir = Path('data_txt')
    txt_files = list(data_dir.glob('*.txt'))
    
    # 存储所有行和统计信息
    all_lines = []
    file_stats = defaultdict(int)
    
    # 读取所有文件内容
    for txt_file in txt_files:
        with open(txt_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            file_stats[txt_file.name] = len(lines)
            all_lines.extend([line.strip() for line in lines])
    
    # 打乱所有行
    random.shuffle(all_lines)
    
    # 写入结果文件
    with open('humor.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_lines))
    
    # 打印统计信息
    print("\n文件统计信息:")
    for filename, count in file_stats.items():
        print(f"{filename}: {count}行")
    print(f"\n总计合并: {len(all_lines)}行")

if __name__ == '__main__':
    merge_and_shuffle_txt()