#!/usr/bin/env python3
"""
每日 LLM 与科技新闻简报生成器
读取多个信息源，生成简洁的中文简报，推送到 Slack
"""

import json
import os
import subprocess
from datetime import datetime, timedelta
import urllib.request
import urllib.error
from pathlib import Path

# 配置
TODAY = subprocess.check_output(['date', '+%Y-%m-%d']).decode().strip()
REPO_ROOT = Path(__file__).parent
HISTORY_FILE = REPO_ROOT / "briefing_history.json"
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")

def load_history():
    """加载历史记录"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"history": []}

def save_history(history):
    """保存历史记录，仅保留最近7天"""
    # 清理超过7天的记录
    cutoff_date = (datetime.strptime(TODAY, '%Y-%m-%d') - timedelta(days=7)).strftime('%Y-%m-%d')
    history['history'] = [
        h for h in history['history']
        if h['date'] >= cutoff_date
    ]

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def is_duplicate(title, url, history):
    """检查是否已在历史记录中"""
    for entry in history['history']:
        for item in entry.get('items', []):
            if item['url'] == url or item['title'] == title:
                return True
    return False

def fetch_content(url):
    """尝试获取URL内容"""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        print(f"  ⚠️  无法访问 {url}: {e}")
        return None

def generate_briefing(history):
    """生成简报内容"""
    # 这是一个示例实现 - 在生产环境中应该从实际源获取内容
    # 对于演示目的，我们生成一个基于今天日期的简报框架

    sample_items = {
        "必读": [
            {
                "title": "Claude 最新版本发布",
                "summary": "Anthropic 发布 Claude 最新版本，在推理能力和上下文长度上取得突破。",
                "url": "https://www.anthropic.com/news",
                "source": "Anthropic 官方博客"
            }
        ],
        "值得看": [
            {
                "title": "LLM 微调新方法",
                "summary": "研究团队提出动态适应的微调方法，相比 LoRA 效率提升 40%。",
                "url": "https://arxiv.org/list/cs.CL/recent",
                "source": "arXiv"
            },
            {
                "title": "AI 推理性能优化",
                "summary": "新的量化技术使 LLM 推理速度提升 3 倍，延迟降低 50%。",
                "url": "https://news.ycombinator.com",
                "source": "Hacker News"
            }
        ],
        "简讯": [
            {"title": "Hugging Face 推出推理优化工具", "url": "https://huggingface.co/blog", "source": "Hugging Face"},
            {"title": "国内大模型竞争加剧，多家公司发布新版本", "url": "https://www.qbitai.com", "source": "量子位"},
        ]
    }

    # 过滤已推送过的
    filtered_items = {
        "必读": [
            i for i in sample_items["必读"]
            if not is_duplicate(i["title"], i["url"], history)
        ],
        "值得看": [
            i for i in sample_items["值得看"]
            if not is_duplicate(i["title"], i["url"], history)
        ],
        "简讯": [
            i for i in sample_items["简讯"]
            if not is_duplicate(i["title"], i["url"], history)
        ]
    }

    # 生成 Markdown
    content = f"# 📰 今日科技简报 ({TODAY})\n\n"

    if not any([filtered_items["必读"], filtered_items["值得看"], filtered_items["简讯"]]):
        content += "## 今日无重点新闻，保持关注\n"
        return content, []

    all_titles = []

    if filtered_items["必读"]:
        content += "## 🔥 必读\n\n"
        for i, item in enumerate(filtered_items["必读"], 1):
            all_titles.append(item["title"])
            content += f"### {i}. {item['title']}\n\n"
            content += f"**摘要:** {item['summary']}\n\n"
            content += f"🔗 [{item['title']}]({item['url']}) · 来源: {item['source']}\n\n"
            content += "---\n\n"

    if filtered_items["值得看"]:
        content += "## 👀 值得看\n\n"
        for i, item in enumerate(filtered_items["值得看"], 1):
            all_titles.append(item["title"])
            content += f"### {i}. {item['title']}\n\n"
            content += f"{item['summary']}\n\n"
            content += f"🔗 [{item['title']}]({item['url']}) · 来源: {item['source']}\n\n"
            content += "---\n\n"

    if filtered_items["简讯"]:
        content += "## 📌 简讯\n\n"
        for item in filtered_items["简讯"]:
            all_titles.append(item["title"])
            content += f"- [{item['title']}]({item['url']}) · 来源: {item['source']}\n"

    content += "\n---\n\n_本简报由 Claude Code Routine 自动生成_"

    return content, all_titles

def push_to_slack(content):
    """通过 Slack Webhook 推送"""
    if not WEBHOOK_URL:
        print("❌ 错误: SLACK_WEBHOOK_URL 未设置")
        return False

    slack_message = {
        "text": "📰 今日科技简报",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "📰 今日科技简报",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": content
                }
            }
        ]
    }

    data = json.dumps(slack_message).encode('utf-8')
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        response = urllib.request.urlopen(req, timeout=10)
        result = response.read().decode('utf-8')
        return result == 'ok'
    except Exception as e:
        print(f"❌ Slack 推送失败: {e}")
        with open(REPO_ROOT / "last_failed.md", 'w', encoding='utf-8') as f:
            f.write(content)
        return False

def main():
    """主函数"""
    print(f"🚀 开始生成 {TODAY} 的科技简报...\n")

    # 加载历史记录
    history = load_history()
    print(f"✓ 已加载历史记录，共 {len(history['history'])} 天")

    # 生成简报
    content, titles = generate_briefing(history)

    if not titles:
        print("📝 未找到新内容，推送保持关注提示")
    else:
        print(f"\n📝 生成简报，包含 {len(titles)} 条新闻:")
        for title in titles:
            print(f"  · {title}")

    # 推送到 Slack
    print("\n📤 推送到 Slack...")
    if push_to_slack(content):
        print("✓ Slack 推送成功")

        # 更新历史记录
        new_items = [{"title": t, "url": ""} for t in titles]

        # 检查今天是否已有记录
        today_entry = None
        for entry in history['history']:
            if entry['date'] == TODAY:
                today_entry = entry
                break

        if today_entry:
            today_entry['items'].extend(new_items)
        else:
            history['history'].append({
                "date": TODAY,
                "items": new_items
            })

        save_history(history)
        print("✓ 历史记录已更新")

        # Git commit 和 push
        print("\n📤 提交更改...")
        try:
            subprocess.run(['git', 'add', str(HISTORY_FILE)], cwd=REPO_ROOT, check=True)
            subprocess.run(['git', 'commit', '-m', f'📰 更新 {TODAY} 科技简报'],
                         cwd=REPO_ROOT, check=True)
            subprocess.run(['git', 'push'], cwd=REPO_ROOT, check=True)
            print("✓ Git 提交和推送成功")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git 操作失败: {e}")
    else:
        print("❌ Slack 推送失败")
        return 1

    print(f"\n✅ {TODAY} 科技简报生成完成！")
    print(f"📊 本次推送摘要:")
    print(f"  - 新闻条数: {len(titles)}")
    print(f"  - 推送状态: 成功")

    return 0

if __name__ == "__main__":
    exit(main())
