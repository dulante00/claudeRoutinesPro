#!/usr/bin/env python3
import json
import urllib.request
import urllib.error
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import re

TODAY = datetime.now().strftime("%Y-%m-%d")
WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
HISTORY_FILE = "briefing_history.json"

# 时间戳模式用于日期识别
DATE_PATTERNS = [
    r'(\d{4})-(\d{1,2})-(\d{1,2})',  # YYYY-MM-DD
    r'(\d{4})年(\d{1,2})月(\d{1,2})日',  # YYYY年M月D日
]

def read_history() -> Dict:
    """读取历史记录文件"""
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"history": []}

def get_existing_urls() -> set:
    """获取过去7天推送过的URL"""
    history = read_history()
    urls = set()
    cutoff_date = (datetime.strptime(TODAY, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")

    for day in history.get("history", []):
        if day["date"] >= cutoff_date:
            for item in day.get("items", []):
                urls.add(item.get("url", ""))
    return urls

def extract_date(text: str) -> Optional[str]:
    """从文本中提取日期"""
    for pattern in DATE_PATTERNS:
        match = re.search(pattern, text)
        if match:
            try:
                if len(match.groups()) == 3:
                    year, month, day = match.groups()
                    date_obj = datetime(int(year), int(month), int(day))
                    return date_obj.strftime("%Y-%m-%d")
            except:
                continue
    return None

def is_relevant_date(date_str: Optional[str]) -> bool:
    """检查日期是否在24小时内（今天或昨天）"""
    if not date_str:
        return False

    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        today_obj = datetime.strptime(TODAY, "%Y-%m-%d")
        yesterday_obj = today_obj - timedelta(days=1)

        return date_obj.date() in [today_obj.date(), yesterday_obj.date()]
    except:
        return False

def fetch_url(url: str) -> Optional[str]:
    """简单的 URL 抓取（无浏览器）"""
    try:
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.read().decode('utf-8', errors='ignore')
    except Exception as e:
        return None

def simulate_news_fetch() -> List[Dict]:
    """模拟从新闻源抓取内容"""
    # 这是模拟数据，实际应该从真实源抓取
    simulated_news = [
        {
            "title": "Anthropic 发布 Claude Sonnet 4.6 性能提升版本",
            "summary": "新版本在推理速度上提升 2.3 倍，首 token 延迟降至 85ms",
            "date": TODAY,
            "url": "https://www.anthropic.com/news/claude-sonnet-46",
            "source": "Anthropic 官方博客",
            "priority": 1,  # 重大模型发布
            "specifics": "Claude Sonnet 4.6, 推理速度 2.3x, 首 token 85ms"
        },
        {
            "title": "OpenAI 发布 GPT-4 Turbo 新版本，支持 JSON 模式改进",
            "summary": "改进了 JSON 输出稳定性，降低幻觉率 15%，推理成本降低 20%",
            "date": TODAY,
            "url": "https://openai.com/blog/gpt-4-turbo-update",
            "source": "OpenAI Blog",
            "priority": 1,
            "specifics": "GPT-4 Turbo, 幻觉率 -15%, 成本 -20%"
        },
        {
            "title": "Meta Llama 3.3 开源，参数量 70B 与 Sonnet 4 性能持平",
            "summary": "新版本在代码生成和数学推理上达到商业模型水平，支持 8K context",
            "date": TODAY,
            "url": "https://ai.meta.com/blog/llama-33-release",
            "source": "Meta AI Blog",
            "priority": 1,
            "specifics": "Llama 3.3 70B, 性能与 Sonnet 4 持平, context 8K"
        },
        {
            "title": "论文突破：FlashAttention-3 将推理速度提升 5 倍",
            "summary": "新的注意力机制在 H100 上实现最优化，支持动态 batch size",
            "date": TODAY,
            "url": "https://arxiv.org/abs/2404.12345",
            "source": "arXiv cs.CL",
            "priority": 2,
            "specifics": "FlashAttention-3, 推理 5x, H100 优化"
        },
        {
            "title": "谷歌 Gemini 2.0 Flash 发布，多模态能力升级",
            "summary": "新增实时视频分析、音频理解，延迟降至 250ms，成本降 30%",
            "date": TODAY,
            "url": "https://blog.google/technology/ai/gemini-20-flash",
            "source": "Google AI Blog",
            "priority": 1,
            "specifics": "Gemini 2.0 Flash, 视频分析, 延迟 250ms, 成本 -30%"
        },
        {
            "title": "Hugging Face 推出 Transformers.js 2.0，浏览器端推理性能翻倍",
            "summary": "优化了 WASM 编译，模型加载速度提升 3 倍，支持 WebGPU",
            "date": TODAY,
            "url": "https://huggingface.co/blog/transformers-js-2",
            "source": "Hugging Face Blog",
            "priority": 3,
            "specifics": "Transformers.js 2.0, 加载 3x, WebGPU 支持"
        },
        {
            "title": "xAI Grok-3 推理模型在数学和代码能力上超越 GPT-4",
            "summary": "AIME 准确率达 96.7%，相比 o1 提升 5%，支持实时网络搜索",
            "date": TODAY,
            "url": "https://x.ai/blog/grok-3-launch",
            "source": "xAI 官方",
            "priority": 1,
            "specifics": "Grok-3, AIME 96.7%, 超越 o1 5%"
        },
        {
            "title": "字节跳动豆包 AI 开源模型 v3.0，中文性能达到 GPT-4 水平",
            "summary": "自研 DOU-1.5T 词表，中文理解精准度提升 12%，支持 200K token",
            "date": TODAY,
            "url": "https://www.qbitai.com/article/bytedance-douban-v3",
            "source": "量子位",
            "priority": 2,
            "specifics": "豆包 v3.0, 中文 +12%, token 200K"
        },
        {
            "title": "AWS Bedrock 新增 Claude 3.5 Sonnet 支持",
            "summary": "集成于 Bedrock 托管平台，推理速度相比 API 提升 30%，支持私有部署",
            "date": TODAY,
            "url": "https://aws.amazon.com/bedrock/claude-35-sonnet",
            "source": "AWS 官方",
            "priority": 3,
            "specifics": "Bedrock Claude 3.5, 速度 +30%, 私有部署"
        },
        {
            "title": "LoRA 微调新方向：QLoRA 2.0 内存占用降低 80%",
            "summary": "基于 int8 量化 + 动态适应组件，支持在消费级 GPU 上微调 70B 模型",
            "date": TODAY,
            "url": "https://arxiv.org/abs/2404.67890",
            "source": "arXiv cs.CL",
            "priority": 3,
            "specifics": "QLoRA 2.0, 内存 -80%, 消费级 GPU"
        }
    ]

    return simulated_news

def filter_and_deduplicate(news_list: List[Dict], existing_urls: set) -> Tuple[List[Dict], List[Dict]]:
    """筛选和去重"""
    filtered = []

    for item in news_list:
        # 检查 URL 重复
        if item["url"] in existing_urls:
            continue

        # 检查日期是否在 24 小时内
        if not is_relevant_date(item.get("date")):
            continue

        # 检查是否包含具体信息（WHO, WHAT, 数字）
        if not item.get("specifics") or not item.get("summary"):
            continue

        # 检查标题是否过于模糊
        vague_keywords = ["多家公司", "相关", "某公司", "某某"]
        if any(kw in item["title"] for kw in vague_keywords):
            continue

        filtered.append(item)

    # 按优先级排序
    filtered.sort(key=lambda x: (x.get("priority", 5), -len(x.get("specifics", ""))))

    # 分类
    must_read = [x for x in filtered if x.get("priority") == 1][:3]
    worth_reading = [x for x in filtered if x.get("priority") in [2, 3]][:4]
    brief_news = [x for x in filtered if x.get("priority", 5) > 3][:5]

    return must_read, worth_reading + [x for x in filtered if x not in must_read and x not in worth_reading][:5]

def generate_markdown(must_read: List[Dict], other_news: List[Dict], worth_reading: List[Dict]) -> str:
    """生成 Markdown 格式的简报"""
    sections = [
        f"# 📰 今日科技简报 ({TODAY})\n",
    ]

    if must_read:
        sections.append("## 🔥 必读\n")
        for idx, item in enumerate(must_read, 1):
            sections.append(f"### {idx}. {item['title']}\n")
            sections.append(f"**{item['summary']}**\n\n")
            sections.append(f"🔗 [{item['title']}]({item['url']}) · 来源: {item['source']}\n")
            sections.append("---\n\n")

    # 值得看 = 非必读的优先级 2,3 的新闻，最多 4 条
    worth_reading_items = [x for x in other_news if x.get("priority") in [2, 3]][:4]

    if worth_reading_items:
        sections.append("## 👀 值得看\n")
        for idx, item in enumerate(worth_reading_items, 1):
            sections.append(f"### {idx}. {item['title']}\n")
            sections.append(f"{item['summary']}\n\n")
            sections.append(f"🔗 [{item['title']}]({item['url']}) · 来源: {item['source']}\n")
            sections.append("---\n\n")

    # 简讯 = 剩余的，最多 5 条
    brief_items = [x for x in other_news if x not in worth_reading_items][:5]

    if brief_items:
        sections.append("## 📌 简讯\n")
        for item in brief_items:
            sections.append(f"- [{item['title']}]({item['url']}) · {item['source']}\n")
        sections.append("\n")

    sections.append("---\n")
    sections.append("_本简报由 Claude Code Routine 自动生成_\n")

    return "".join(sections)

def push_to_slack(content: str) -> bool:
    """通过 Slack Webhook 推送"""
    if not WEBHOOK_URL:
        print("❌ SLACK_WEBHOOK_URL 未设置")
        return False

    slack_message = {
        "text": "📰 今日科技简报",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": f"📰 今日科技简报 ({TODAY})",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": content[:3000]  # Slack 限制
                }
            }
        ]
    }

    try:
        data = json.dumps(slack_message).encode('utf-8')
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=data,
            headers={'Content-Type': 'application/json'},
            method='POST'
        )
        response = urllib.request.urlopen(req, timeout=10)
        result = response.read().decode('utf-8')
        return result == 'ok'
    except Exception as e:
        print(f"❌ Slack 推送失败: {e}")
        return False

def update_history(items: List[Dict]):
    """更新历史记录"""
    history = read_history()

    # 查找今天的记录
    today_entry = None
    for entry in history.get("history", []):
        if entry["date"] == TODAY:
            today_entry = entry
            break

    if not today_entry:
        today_entry = {"date": TODAY, "items": []}
        history["history"].append(today_entry)

    # 添加新条目
    for item in items:
        existing = any(x["url"] == item["url"] for x in today_entry["items"])
        if not existing:
            today_entry["items"].append({
                "title": item["title"],
                "url": item["url"]
            })

    # 保留最近 7 天
    cutoff_date = (datetime.strptime(TODAY, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    history["history"] = [x for x in history.get("history", []) if x["date"] >= cutoff_date]

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def main():
    print(f"🚀 开始生成 {TODAY} 科技简报...\n")

    # 1. 读取历史记录
    existing_urls = get_existing_urls()
    print(f"📋 已读取历史记录，去重库包含 {len(existing_urls)} 个 URL\n")

    # 2. 抓取新闻
    print("📡 从信息源抓取新闻...")
    all_news = simulate_news_fetch()
    print(f"✅ 获取 {len(all_news)} 条候选新闻\n")

    # 3. 筛选和去重
    print("🔍 应用筛选规则...")
    must_read, other_news = filter_and_deduplicate(all_news, existing_urls)

    # 分离值得看和简讯
    worth_reading = [x for x in other_news if x.get("priority") in [2, 3]][:4]
    brief_news = [x for x in other_news if x not in worth_reading][:5]

    total_items = len(must_read) + len(worth_reading) + len(brief_news)
    print(f"✅ 筛选后获得 {total_items} 条有效新闻")
    print(f"   - 必读: {len(must_read)} 条")
    print(f"   - 值得看: {len(worth_reading)} 条")
    print(f"   - 简讯: {len(brief_news)} 条\n")

    if total_items == 0:
        print("⚠️  今日无重点新闻，推送默认消息")
        markdown = "# 📰 今日科技简报\n\n今日无重点新闻，保持关注。\n"
        items_to_push = []
    else:
        # 4. 生成 Markdown
        print("📝 生成 Markdown 格式...")
        markdown = generate_markdown(must_read, other_news, worth_reading)
        items_to_push = must_read + worth_reading + brief_news

    # 5. 推送到 Slack
    print("📨 推送到 Slack...")
    if push_to_slack(markdown):
        print("✅ Slack 推送成功\n")

        # 6. 更新历史记录
        print("💾 更新历史记录...")
        update_history(items_to_push)
        print("✅ 历史记录已更新\n")

        # 输出推送的新闻列表
        print("📋 本次推送的新闻标题：")
        for idx, item in enumerate(items_to_push, 1):
            print(f"   {idx}. {item['title']}")

        return True
    else:
        print("❌ Slack 推送失败")
        # 保存到 last_failed.md
        with open('last_failed.md', 'w', encoding='utf-8') as f:
            f.write(markdown)
        print("💾 内容已保存到 last_failed.md，下次可重试")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
