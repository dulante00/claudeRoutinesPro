#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import urllib.request
import os
from datetime import datetime, timedelta

# Configuration
TODAY = "2026-04-22"
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")
HISTORY_FILE = "briefing_history.json"

# Load existing history for deduplication
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"history": []}

# Extract titles and URLs from today's history
def get_existing_urls():
    history = load_history()
    existing = set()
    for day in history.get("history", []):
        for item in day.get("items", []):
            existing.add(item.get("url", ""))
    return existing

# Generate briefing content
def generate_briefing():
    existing_urls = get_existing_urls()

    # Today's news items (from WebSearch results, excluding duplicates)
    items = [
        {
            "title": "Claude Opus 4.7 正式发布 - 性能与成本大幅优化",
            "summary": "Anthropic 发布 Claude Opus 4.7，这是其最强大的通用模型，支持高达 2576px/3.75MP 的高分辨率图像，新增 xhigh effort 级别以优化成本与延迟权衡，并推出 beta 任务预算功能，可在代理循环中管理 token 消耗。",
            "category": "🔥",
            "url": "https://www.anthropic.com/news",
            "source": "Anthropic 官方博客",
            "date": "2026-04-16"
        },
        {
            "title": "Claude Design 上线 - AI 生成视觉创意工具",
            "summary": "Anthropic 推出 Claude Design，一款 AI 原生视觉创意工具，支持快速生成原型、演示稿、一页纸等设计资产。通过 Chat-to-Design 概念，用户可通过对话、评论、直接编辑与自定义滑块进行迭代。",
            "category": "👀",
            "url": "https://techcrunch.com/2026/04/17/anthropic-launches-claude-design-a-new-product-for-creating-quick-visuals/",
            "source": "TechCrunch"
        },
        {
            "title": "GPT-6 官宣发布 - 性能提升 40%，定价大幅下调",
            "summary": "OpenAI 官方确认 GPT-6（代号 Spud）于 4 月 14 日全球发布。核心亮点：200 万 token 上下文窗口（为 GPT-5 的 4 倍）、性能提升 40%，同时 API 定价仅为前代 50%（输入 $2.5/百万 token）。架构采用全新 Symphony 架构，原生多模态统一。",
            "category": "🔥",
            "url": "https://news.qq.com/rain/a/20260409A021OB00",
            "source": "腾讯新闻"
        },
        {
            "title": "2026 中国生成式 AI 大会进行中 - 两天技术研讨密集举行",
            "summary": "2026 中国生成式 AI 大会（北京）4 月 21-22 日进行。4 月 22 日议程包含 LLM 强化学习、推理系统、端侧大模型部署、视频生成等 4 场技术研讨会，汇聚 70+ 重量级嘉宾。",
            "category": "👀",
            "url": "https://zhidx.com/p/529512.html",
            "source": "智东西"
        },
        {
            "title": "中国 AI 大模型调用量连续五周超越美国",
            "summary": "上周中国 AI 大模型周调用量上升至 12.96 万亿 Token，环比增长 31.48%；美国仅 3.03 万亿 Token。中国大模型生态调用量已连续 5 周超越美国，展示国内 AI 应用的强劲势头。",
            "category": "📌",
            "url": "https://finance.sina.com.cn/stock/bxjj/2026-04-06/doc-inhtpmek1508270.shtml",
            "source": "新浪财经"
        },
        {
            "title": "TurboAgent - LLM 多代理框架解决复杂工程设计",
            "summary": "arXiv 最新论文：TurboAgent 实现 LLM 驱动的自主多代理框架，可在 30 分钟内完成涡轮机械气动设计全流程闭环优化，大幅提升性能指标。",
            "category": "📌",
            "url": "https://arxiv.org/list/cs.AI/new",
            "source": "arXiv"
        }
    ]

    # Filter by URL deduplication and date
    filtered_items = []
    for item in items:
        if item["url"] not in existing_urls:
            filtered_items.append(item)

    if not filtered_items:
        return "今日无新增重点新闻，保持关注", []

    # Organize by priority
    must_read = [i for i in filtered_items if i["category"] == "🔥"][:3]
    worth_reading = [i for i in filtered_items if i["category"] == "👀"][:4]
    brief_news = [i for i in filtered_items if i["category"] == "📌"][:5]

    # Generate Markdown
    markdown = f"# 📰 今日科技简报 ({TODAY})\n\n"

    if must_read:
        markdown += "## 🔥 必读\n\n"
        for idx, item in enumerate(must_read, 1):
            markdown += f"### {idx}. {item['title']}\n"
            markdown += f"**{item['summary'][:50]}**\n\n"
            markdown += f"{item['summary'][50:]}\n\n"
            markdown += f"🔗 [{item['title']}]({item['url']}) · 来源: {item['source']}\n\n---\n\n"

    if worth_reading:
        markdown += "## 👀 值得看\n\n"
        for idx, item in enumerate(worth_reading, 1):
            markdown += f"### {idx}. {item['title']}\n"
            markdown += f"{item['summary']}\n\n"
            markdown += f"🔗 [{item['title']}]({item['url']}) · 来源: {item['source']}\n\n---\n\n"

    if brief_news:
        markdown += "## 📌 简讯\n\n"
        for item in brief_news:
            markdown += f"- [{item['title']}]({item['url']}) · {item['source']}\n"

    markdown += "\n---\n\n_本简报由 Claude Code Routine 自动生成_"

    return markdown, filtered_items

# Push to Slack
def push_to_slack(content):
    if not SLACK_WEBHOOK_URL:
        print("❌ 错误：SLACK_WEBHOOK_URL 未设置")
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
                    "text": content[:3000]  # Slack 限制
                }
            }
        ]
    }

    data = json.dumps(slack_message).encode('utf-8')
    req = urllib.request.Request(
        SLACK_WEBHOOK_URL,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )

    try:
        response = urllib.request.urlopen(req)
        result = response.read().decode('utf-8')
        return result == 'ok'
    except Exception as e:
        print(f"❌ Slack 推送失败: {e}")
        return False

# Update history
def update_history(items):
    history = load_history()

    # Remove old entries beyond 7 days
    cutoff_date = (datetime.strptime(TODAY, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    history["history"] = [h for h in history["history"] if h.get("date", "") >= cutoff_date]

    # Add today's entries
    today_entry = {
        "date": TODAY,
        "items": [{"title": i["title"], "url": i["url"]} for i in items]
    }

    # Check if today already exists
    found = False
    for h in history["history"]:
        if h["date"] == TODAY:
            h["items"].extend(today_entry["items"])
            found = True
            break

    if not found:
        history["history"].append(today_entry)

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# Main
if __name__ == "__main__":
    print(f"🔄 生成 {TODAY} 的科技简报...\n")

    content, items = generate_briefing()

    if not items:
        print("✅ 已发现内容：今日无新增重点新闻")
        push_to_slack("📰 今日无新增重点新闻，保持关注")
    else:
        print(f"✅ 已生成 {len(items)} 条新闻摘要\n")
        print("📰 今日推送标题列表：")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item['title']}")

        if push_to_slack(content):
            print("\n✅ 已成功推送到 Slack")
        else:
            print("\n❌ Slack 推送失败，保存到 last_failed.md")
            with open("last_failed.md", 'w', encoding='utf-8') as f:
                f.write(content)

        # Always update history regardless of Slack push success
        update_history(items)
        print("✅ 已更新历史记录")
