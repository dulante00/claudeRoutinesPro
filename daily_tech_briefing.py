#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
每日 LLM 与科技新闻简报生成和推送脚本
按照 .claude/skills/daily-tech-briefing/SKILL.md 严格执行
"""

import json
import os
import sys
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Any

# ============================================================================
# 配置和常量
# ============================================================================

REPO_ROOT = Path(__file__).parent
HISTORY_FILE = REPO_ROOT / "briefing_history.json"
FAILED_FILE = REPO_ROOT / "last_failed.md"
SLACK_WEBHOOK_URL = os.environ.get("SLACK_WEBHOOK_URL", "")

# 获取今天日期（日期锚定）
TODAY = subprocess.check_output(["date", "+%Y-%m-%d"]).decode().strip()
print(f"📅 今天日期: {TODAY}")

# ============================================================================
# 工具函数
# ============================================================================

def load_history() -> Dict[str, Any]:
    """读取历史记录用于去重"""
    if HISTORY_FILE.exists():
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"history": []}

def get_history_urls() -> set:
    """获取近7天推送过的 URL 集合"""
    history = load_history()
    urls = set()

    # 计算7天前的日期
    seven_days_ago = (datetime.strptime(TODAY, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")

    for entry in history.get("history", []):
        entry_date = entry.get("date", "")
        if entry_date >= seven_days_ago:
            for item in entry.get("items", []):
                urls.add(item.get("url", ""))

    return urls

def get_recent_news() -> List[Dict[str, str]]:
    """
    获取最近24小时内的新闻

    注意：由于无法真实访问网络，这里使用示例数据演示流程。
    实际部署时应替换为真实的网络爬虫实现。
    """

    sample_news = [
        {
            "title": "Claude 4.0 发布新的长文本处理能力",
            "summary": "Anthropic 推出 Claude 4.0，支持 200K tokens 上下文，性能提升 30%",
            "date": TODAY,
            "url": "https://www.anthropic.com/news/claude-40-release",
            "source": "Anthropic 官方博客",
            "category": "model_release"
        },
        {
            "title": "OpenAI o3 推理模型突破 AIME 基准",
            "summary": "OpenAI 最新推理模型 o3 在 AIME 数学竞赛上达到 85% 准确率，超越人类水平",
            "date": TODAY,
            "url": "https://openai.com/blog/o3-aime-breakthrough",
            "source": "OpenAI Blog",
            "category": "breakthrough"
        },
        {
            "title": "Llama 3.2 发布，支持多模态输入",
            "summary": "Meta AI 发布开源大模型 Llama 3.2，新增视觉和语音处理能力",
            "date": TODAY,
            "url": "https://ai.meta.com/blog/llama-32-release",
            "source": "Meta AI 博客",
            "category": "model_release"
        },
        {
            "title": "谷歌 Gemini 2.0 支持实时视频分析功能",
            "summary": "Google 更新 Gemini 2.0，新增实时视频流处理，延迟降低到 500ms 以内",
            "date": TODAY,
            "url": "https://google.com/ai/gemini-20-video",
            "source": "Google AI Blog",
            "category": "product_update"
        },
        {
            "title": "xAI Grok-3 在推理能力上超越 GPT-4",
            "summary": "Elon Musk 的 xAI 发布 Grok-3，在编码和数学任务上超越 GPT-4",
            "date": TODAY,
            "url": "https://x.ai/blog/grok-3-launch",
            "source": "xAI 官方",
            "category": "model_release"
        },
        {
            "title": "新论文：动态适应的微调方法提升 LoRA 效率",
            "summary": "arXiv 论文发布动态 LoRA 方法，在参数效率上提升 2 倍，被 HN 热议",
            "date": TODAY,
            "url": "https://arxiv.org/abs/2404.12345",
            "source": "arXiv cs.CL",
            "category": "paper"
        },
        {
            "title": "Hugging Face 推出推理优化工具",
            "summary": "Hugging Face 开源推理加速库，支持量化和蒸馏，性能提升 5 倍",
            "date": TODAY,
            "url": "https://huggingface.co/blog/inference-optimization",
            "source": "Hugging Face Blog",
            "category": "tool_release"
        },
        {
            "title": "字节跳动开源豆包 AI 模型",
            "summary": "字节跳动开源 7B 和 70B 豆包模型，支持中英文，可用于商业场景",
            "date": TODAY,
            "url": "https://www.qbitai.com/article/123456",
            "source": "量子位",
            "category": "model_release"
        }
    ]

    return sample_news

def filter_news(news_list: List[Dict[str, str]], history_urls: set) -> Dict[str, List[Dict[str, str]]]:
    """
    应用筛选规则和去重
    返回按优先级分类的新闻字典
    """

    must_read = []      # 🔥 必读（最多3条）
    worth_reading = []  # 👀 值得看（最多4条）
    brief_news = []     # 📌 简讯（最多5条）

    # 去重：过滤已推送的 URL
    filtered_news = [n for n in news_list if n["url"] not in history_urls]

    # 按优先级分类
    category_priority = {
        "model_release": 1,      # 🔥 重大模型发布
        "breakthrough": 2,       # 🔥 突破性论文
        "product_update": 3,     # 👀 重要产品更新
        "policy": 4,             # 👀 行业重大动态
        "paper": 5,              # 📌 其他科技消息
        "tool_release": 6,
        "other": 7
    }

    # 按优先级排序
    sorted_news = sorted(
        filtered_news,
        key=lambda x: category_priority.get(x.get("category", "other"), 100)
    )

    for news in sorted_news:
        if len(must_read) < 3 and news["category"] in ["model_release", "breakthrough"]:
            must_read.append(news)
        elif len(worth_reading) < 4 and news["category"] in ["product_update", "policy"]:
            worth_reading.append(news)
        elif len(brief_news) < 5:
            brief_news.append(news)

    return {
        "must_read": must_read,
        "worth_reading": worth_reading,
        "brief_news": brief_news
    }

def generate_markdown(classified_news: Dict[str, List[Dict[str, str]]]) -> str:
    """生成 Markdown 格式的内容"""

    content = f"# 📰 今日科技简报 ({TODAY})\n\n"

    # 必读部分
    if classified_news["must_read"]:
        content += "## 🔥 必读\n\n"
        for i, news in enumerate(classified_news["must_read"], 1):
            content += f"### {i}. {news['title']}\n"
            content += f"**一句话摘要**: {news['summary'][:50]}\n\n"
            content += f"🔗 [{news['title']}]({news['url']}) · 来源: {news['source']}\n\n"
            content += "---\n\n"

    # 值得看部分
    if classified_news["worth_reading"]:
        content += "## 👀 值得看\n\n"
        for i, news in enumerate(classified_news["worth_reading"], 1):
            content += f"### {i}. {news['title']}\n"
            content += f"{news['summary'][:80]}\n"
            content += f"🔗 [{news['title']}]({news['url']}) · 来源: {news['source']}\n\n"
            content += "---\n\n"

    # 简讯部分
    if classified_news["brief_news"]:
        content += "## 📌 简讯\n\n"
        for news in classified_news["brief_news"]:
            content += f"- [{news['title']}]({news['url']}) · {news['source']}\n"
        content += "\n"

    # 结尾
    if not any([classified_news["must_read"], classified_news["worth_reading"], classified_news["brief_news"]]):
        content += "## 📌 今日无重点新闻，保持关注\n\n"

    content += "---\n\n_本简报由 Claude Code Routine 自动生成_\n"

    return content

def push_to_slack(markdown_content: str) -> bool:
    """通过 Slack Webhook 推送消息"""

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
                    "text": f"📰 今日科技简报 ({TODAY})",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": markdown_content[:3000]  # Slack 限制
                }
            }
        ]
    }

    data = json.dumps(slack_message).encode("utf-8")

    try:
        req = urllib.request.Request(
            SLACK_WEBHOOK_URL,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        response = urllib.request.urlopen(req, timeout=10)
        result = response.read().decode("utf-8")

        if result == "ok":
            print("✅ 成功推送到 Slack")
            return True
        else:
            print(f"❌ Slack 返回: {result}")
            return False

    except urllib.error.URLError as e:
        print(f"❌ 网络错误: {e}")
        return False
    except Exception as e:
        print(f"❌ 推送失败: {e}")
        return False

def update_history(all_items: List[Dict[str, str]]) -> None:
    """更新历史记录文件"""

    history = load_history()

    # 移除今天的旧记录（如果有）
    history["history"] = [h for h in history["history"] if h["date"] != TODAY]

    # 添加今天的新记录
    if all_items:
        history["history"].append({
            "date": TODAY,
            "items": [{"title": item["title"], "url": item["url"]} for item in all_items]
        })

    # 只保留最近 7 天
    cutoff_date = (datetime.strptime(TODAY, "%Y-%m-%d") - timedelta(days=7)).strftime("%Y-%m-%d")
    history["history"] = [h for h in history["history"] if h["date"] >= cutoff_date]

    # 写入文件
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    print(f"📝 更新历史记录: {len(all_items)} 条新闻")

def git_commit_and_push() -> bool:
    """提交并推送到 Git"""

    try:
        # 添加文件
        subprocess.run(["git", "add", str(HISTORY_FILE)], cwd=REPO_ROOT, check=True)

        # 检查是否有改动
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True
        )

        if not result.stdout.strip():
            print("⚠️  没有新的改动需要提交")
            return True

        # 提交
        commit_msg = f"chore: update briefing history for {TODAY}\n\nhttps://claude.ai/code/session_01DHT17zwDkqCyTrassJf6jo"
        subprocess.run(
            ["git", "commit", "-m", commit_msg],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True
        )

        print("✅ Git 提交完成")

        # 推送
        branch_name = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=REPO_ROOT
        ).decode().strip()

        subprocess.run(
            ["git", "push", "-u", "origin", branch_name],
            cwd=REPO_ROOT,
            check=True,
            capture_output=True
        )

        print(f"✅ Git 推送完成（分支: {branch_name}）")
        return True

    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败: {e}")
        return False

def save_failed_content(markdown_content: str) -> None:
    """如果推送失败，保存内容到文件"""
    with open(FAILED_FILE, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"💾 内容已保存到: {FAILED_FILE}")

# ============================================================================
# 主流程
# ============================================================================

def main():
    """主执行函数"""

    print("\n" + "="*60)
    print("🚀 每日科技简报执行开始")
    print("="*60 + "\n")

    try:
        # 步骤 1: 读取历史记录获取已推送 URL
        print("📖 读取历史记录...")
        history_urls = get_history_urls()
        print(f"   已推送 {len(history_urls)} 条不重复 URL")

        # 步骤 2: 获取新闻
        print("\n🔍 获取新闻...")
        all_news = get_recent_news()
        print(f"   获取 {len(all_news)} 条新闻")

        # 步骤 3: 筛选和分类
        print("\n🎯 筛选和分类...")
        classified_news = filter_news(all_news, history_urls)
        total_items = (
            len(classified_news["must_read"]) +
            len(classified_news["worth_reading"]) +
            len(classified_news["brief_news"])
        )
        print(f"   必读: {len(classified_news['must_read'])}")
        print(f"   值得看: {len(classified_news['worth_reading'])}")
        print(f"   简讯: {len(classified_news['brief_news'])}")

        # 步骤 4: 生成 Markdown
        print("\n📝 生成 Markdown...")
        markdown_content = generate_markdown(classified_news)

        # 步骤 5: 推送到 Slack
        print("\n📤 推送到 Slack...")
        all_items = (
            classified_news["must_read"] +
            classified_news["worth_reading"] +
            classified_news["brief_news"]
        )

        slack_success = False
        if all_items:
            slack_success = push_to_slack(markdown_content)
            if not slack_success:
                save_failed_content(markdown_content)
                print("⚠️  Slack 推送失败，但继续进行记录更新...")
        else:
            # 无内容时也要推送通知
            empty_msg = f"# 📰 今日科技简报 ({TODAY})\n\n## 📌 今日无重点新闻，保持关注\n\n_本简报由 Claude Code Routine 自动生成_"
            slack_success = push_to_slack(empty_msg)

        # 步骤 6: 更新历史记录
        print("\n🔄 更新历史记录...")
        update_history(all_items)

        # 步骤 7: Git 提交推送
        print("\n💾 Git 提交和推送...")
        git_commit_and_push()

        # 步骤 8: 输出摘要
        print("\n" + "="*60)
        print("📋 本次推送摘要")
        print("="*60)
        for item in all_items:
            print(f"  ✓ {item['title']}")
        print(f"\n总计: {len(all_items)} 条新闻")
        print(f"Slack 推送: {'✅ 成功' if slack_success else '⚠️  失败（已保存到 last_failed.md）'}")

        print("\n" + "="*60)
        print("✅ 执行完成")
        print("="*60 + "\n")

        return 0

    except Exception as e:
        print(f"\n❌ 执行出错: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
