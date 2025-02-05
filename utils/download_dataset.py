import os
import json
import argparse
from datasets import load_dataset
from operator import itemgetter
from tqdm import tqdm
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser(description='下载并处理笑话数据集')
    parser.add_argument('--total', type=int, default=50, help='下载的总条数')
    parser.add_argument('--select', type=int, default=20, help='选择score最高的条数')
    parser.add_argument('--plot', action='store_true', help='是否绘制score分布图')
    return parser.parse_args()

def plot_score_distribution(scores, output_path="score_distribution.png"):
    plt.figure(figsize=(10, 6))
    plt.hist(scores, bins=20, edgecolor='black')
    plt.title('Score Distribution of Selected Jokes')
    plt.xlabel('Score')
    plt.ylabel('Frequency')
    plt.savefig(output_path)
    plt.close()
    print(f"分数分布图已保存至: {output_path}")

def main():
    args = parse_args()
    
    # 获取 Hugging Face 令牌
    hf_token = os.getenv("HF_TOKEN")
    if not hf_token:
        raise ValueError("请设置 HF_TOKEN 环境变量")

    # 下载数据集
    print(f"正在下载前{args.total}条数据...")
    dataset = load_dataset("kuldin/english_jokes", split="train", token=hf_token).select(range(args.total))

    # 转换为列表并按score排序
    jokes_list = [
        {
            'id': item['id'],
            'score': item['score'],
            'title': item['title'],
            'body': item['body']
        }
        for item in tqdm(dataset, desc="处理数据")
    ]
    sorted_jokes = sorted(jokes_list, key=itemgetter('score'), reverse=True)

    # 选择前N条转换格式
    formatted_data = []
    for item in tqdm(sorted_jokes[:args.select], desc="格式转换"):
        joke = item["title"] if item["body"] == "" else item["body"]
        formatted_data.append({
            "system": "You are a witty AI assistant who always responds humorously.",
            "instruction": f"User: {item['title']}",
            "input": "",
            "output": joke
        })

    # 保存为JSON
    output_path = "jokes_conversation.json"
    with open(output_path, "w", encoding='utf-8') as f:
        json.dump(formatted_data, f, indent=4, ensure_ascii=False)

    print(f"已处理完成，选择了score最高的{len(formatted_data)}条笑话")
    print(f"数据已保存至: {output_path}")

    # 如果需要绘制分布图
    if args.plot:
        selected_scores = [joke['score'] for joke in sorted_jokes[:args.select]]
        plot_score_distribution(selected_scores)

if __name__ == "__main__":
    main()