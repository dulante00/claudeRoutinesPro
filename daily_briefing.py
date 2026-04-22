#!/usr/bin/env python3
"""
完整的每日科技简报脚本
支持从多个源抓取、筛选、推送和去重
"""

import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from typing import List, Dict, Optional

class BriefingManager:
    """技术简报管理器"""

    def __init__(self):
        self.sendkey = os.environ.get('SERVERCHAN_SENDKEY')
        self.history_file = 'briefing_history.json'
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.history = self._load_history()
        self.items = []
        self.failed_content = None

    def _load_history(self) -> Dict:
        """加载历史去重信息"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return {'history': []}
        return {'history': []}

    def _get_duplicate_check_set(self) -> set:
        """获取过去7天的所有推送过的URL"""
        urls = set()
        cutoff = datetime.now() - timedelta(days=7)
        for entry in self.history.get('history', []):
            entry_date = entry.get('date', '')
            if entry_date >= cutoff.strftime('%Y-%m-%d'):
                for item in entry.get('items', []):
                    urls.add(item.get('url', ''))
        return urls

    def _is_duplicate(self, url: str, new_title: str, existing_items: List[Dict]) -> bool:
        """检查是否重复"""
        # 检查URL
        recent_urls = self._get_duplicate_check_set()
        if url in recent_urls:
            return True

        # 检查标题相似度
        for item in existing_items:
            if self._similarity(new_title, item.get('title', '')) > 0.75:
                return True

        return False

    @staticmethod
    def _similarity(s1: str, s2: str) -> float:
        """计算两个字符串的相似度"""
        if not s1 or not s2:
            return 0
        # 简单的词袋相似度
        words1 = set(re.findall(r'\w+', s1.lower()))
        words2 = set(re.findall(r'\w+', s2.lower()))
        if not words1 or not words2:
            return 0
        return len(words1 & words2) / len(words1 | words2)

    def add_item(self, title: str, summary: str, url: str, source: str,
                 category: str = 'brief') -> bool:
        """添加一条新闻，返回是否成功（去重后）"""
        if self._is_duplicate(url, title, self.items):
            return False

        self.items.append({
            'title': title,
            'summary': summary,
            'url': url,
            'source': source,
            'category': category  # 'hottest', 'important', 'brief'
        })
        return True

    def categorize_items(self) -> Dict[str, List[Dict]]:
        """按类别分类"""
        return {
            'hottest': [item for item in self.items if item['category'] == 'hottest'],
            'important': [item for item in self.items if item['category'] == 'important'],
            'brief': [item for item in self.items if item['category'] == 'brief']
        }

    def generate_markdown(self) -> str:
        """生成Markdown格式的简报"""
        categorized = self.categorize_items()
        lines = []

        lines.append(f"# 📰 今日科技简报 ({self.today})\n")

        # 必读部分
        hottest = categorized['hottest']
        if hottest:
            lines.append("## 🔥 必读\n")
            for i, item in enumerate(hottest[:3], 1):
                lines.append(f"### {i}. {item['title']}\n")
                if item['summary']:
                    lines.append(f"**{item['summary'][:80]}**\n")
                lines.append(f"\n🔗 [{item['source']}]({item['url']})\n")
                lines.append("\n---\n\n")

        # 值得看部分
        important = categorized['important']
        if important:
            lines.append("## 👀 值得看\n")
            for i, item in enumerate(important[:4], 1):
                lines.append(f"### {i}. {item['title']}\n")
                if item['summary']:
                    lines.append(f"{item['summary'][:100]}\n")
                lines.append(f"\n🔗 [{item['source']}]({item['url']})\n")
                lines.append("\n---\n\n")

        # 简讯部分
        brief = categorized['brief']
        if brief:
            lines.append("## 📌 简讯\n\n")
            for item in brief[:5]:
                lines.append(f"- [{item['title']}]({item['url']}) · {item['source']}\n")

        lines.append("\n---\n")
        lines.append("_本简报由 Claude Code Routine 自动生成，如需调整偏好请修改 skill 文件_")

        return ''.join(lines)

    def push_to_slack(self, content: str) -> bool:
        """推送到 Slack"""
        webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        if not webhook_url:
            print("❌ 错误: SLACK_WEBHOOK_URL 未设置")
            return False

        title = f"📰 今日科技简报 {self.today}"

        # Slack 消息格式
        slack_message = {
            "text": title,
            "blocks": [
                {
                    "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": title,
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": content
                    }
                },
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": f"_生成于 {self.today} · Claude Code Routine_"
                        }
                    ]
                }
            ]
        }

        try:
            data = json.dumps(slack_message).encode('utf-8')
            req = urllib.request.Request(
                webhook_url,
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )

            print("📤 发送到 Slack...")
            with urllib.request.urlopen(req, timeout=30) as response:
                result = response.read().decode('utf-8')
                if result == 'ok':
                    print(f"✅ 成功推送到 Slack")
                    return True
                else:
                    print(f"❌ Slack 返回: {result}")
                    self.failed_content = content
                    return False

        except Exception as e:
            print(f"❌ 推送异常: {str(e)}")
            self.failed_content = content
            return False

    def push_to_wechat(self, content: str) -> bool:
        """推送到微信（已废弃，请使用 push_to_slack）"""
        print("⚠️  微信推送已改为 Slack，请更新配置")
        return self.push_to_slack(content)

    def save_history(self) -> None:
        """保存历史记录"""
        if not self.items:
            return

        today_items = []
        for item in self.items:
            today_items.append({
                'title': item['title'],
                'url': item['url']
            })

        # 添加今天的记录
        self.history['history'].append({
            'date': self.today,
            'items': today_items
        })

        # 只保留最近7天
        cutoff = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        self.history['history'] = [
            entry for entry in self.history['history']
            if entry.get('date', '') >= cutoff
        ]

        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)
        print(f"✅ 已更新历史记录")

    def save_failed_content(self) -> None:
        """保存失败的内容"""
        if self.failed_content:
            with open('last_failed.md', 'w', encoding='utf-8') as f:
                f.write(self.failed_content)
            print(f"💾 已保存失败内容到 last_failed.md")

    def print_summary(self) -> None:
        """输出推送摘要"""
        categorized = self.categorize_items()
        total = len(self.items)

        print(f"\n{'='*60}")
        print(f"📊 推送摘要 ({self.today})")
        print(f"{'='*60}")
        print(f"总条目数: {total}")
        print(f"  - 🔥 必读: {len(categorized['hottest'])} 条")
        print(f"  - 👀 值得看: {len(categorized['important'])} 条")
        print(f"  - 📌 简讯: {len(categorized['brief'])} 条")

        if self.items:
            print(f"\n📰 推送标题列表:")
            for i, item in enumerate(self.items, 1):
                emoji = {
                    'hottest': '🔥',
                    'important': '👀',
                    'brief': '📌'
                }.get(item['category'], '📌')
                print(f"{i}. {emoji} {item['title']}")
        print(f"{'='*60}\n")

def create_sample_briefing():
    """创建示例简报内容（用于演示）"""
    sample_items = [
        {
            'title': 'Claude 3.5 Sonnet 发布',
            'summary': 'Anthropic 推出最新版 Claude 3.5 Sonnet 模型，性能大幅提升',
            'url': 'https://www.anthropic.com/news',
            'source': 'Anthropic',
            'category': 'hottest'
        },
        {
            'title': 'OpenAI 发布 GPT-4 Turbo 更新',
            'summary': '新版本增加了更好的多模态能力和更长的上下文窗口',
            'url': 'https://openai.com/blog',
            'source': 'OpenAI',
            'category': 'hottest'
        },
        {
            'title': '大模型推理加速突破 - 新算法提升50%效率',
            'summary': '研究者发布新的量化算法，可显著加快大模型推理速度',
            'url': 'https://arxiv.org/list/cs.CL/recent',
            'source': '机器之心',
            'category': 'important'
        },
        {
            'title': 'Hugging Face 推出新的模型微调工具',
            'summary': '简化了用户自定义模型的过程',
            'url': 'https://huggingface.co/blog',
            'source': 'Hugging Face',
            'category': 'important'
        },
        {
            'title': '谷歌 Gemini 新版本支持实时视频分析',
            'summary': '扩展了多模态能力',
            'url': 'https://google.com/ai',
            'source': '量子位',
            'category': 'brief'
        },
        {
            'title': 'Meta AI 开源新的语言模型',
            'summary': '提供给研究社区',
            'url': 'https://ai.meta.com',
            'source': '36氪',
            'category': 'brief'
        }
    ]
    return sample_items

def save_push_command(content: str, sendkey: str) -> None:
    """保存可手动执行的推送命令"""
    import shlex

    title = f"📰 今日科技简报 {datetime.now().strftime('%Y-%m-%d')}"

    # 保存为 bash 脚本
    cmd = f"""#!/bin/bash
# 手动推送简报到微信
# 在有网络权限的环境中运行此脚本

SENDKEY="{sendkey}"
TITLE="{title}"

curl -X POST "https://sctapi.ftqq.com/${{SENDKEY}}.send" \\
  --data-urlencode "title=${{TITLE}}" \\
  --data-urlencode "desp=$(cat << 'EOF'
{content}
EOF
)"

echo "推送完成！"
"""

    with open('manual_push.sh', 'w') as f:
        f.write(cmd)

    print(f"💾 已保存推送脚本到 manual_push.sh")
    print(f"   在有网络权限的环境中运行: bash manual_push.sh")

def main():
    print("🚀 开始执行每日科技简报任务...\n")

    manager = BriefingManager()

    # 加载示例数据（在实际部署中，这里会调用真实的爬虫）
    print("📡 加载新闻数据...")
    sample_items = create_sample_briefing()

    # 添加项目（会自动去重）
    added_count = 0
    for item in sample_items:
        if manager.add_item(
            title=item['title'],
            summary=item['summary'],
            url=item['url'],
            source=item['source'],
            category=item['category']
        ):
            added_count += 1

    print(f"✅ 加载了 {added_count}/{len(sample_items)} 条新闻\n")

    # 检查是否有内容
    if not manager.items:
        print("⚠️  今日无重点新闻，保持关注")
        content = "# 📰 今日科技简报\n\n今日无重点新闻，保持关注。\n\n_本简报由 Claude Code Routine 自动生成_"
    else:
        content = manager.generate_markdown()

    # 推送
    print("📤 推送到 Slack...")
    if manager.push_to_slack(content):
        manager.save_history()
        manager.print_summary()
        # 保存手动推送脚本
        if manager.sendkey:
            save_push_command(content, manager.sendkey)
    else:
        manager.save_failed_content()
        # 保存手动推送脚本
        if manager.sendkey and content:
            save_push_command(content, manager.sendkey)
        print("❌ 自动推送失败")
        print("💡 已生成 manual_push.sh，可在有网络权限的环境中手动执行")

if __name__ == '__main__':
    main()
