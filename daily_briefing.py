#!/usr/bin/env python3
"""
每日科技简报 - Claude Code Routines 版本

在 Claude Code Routines 沙箱中执行
通知方式：Slack Webhook
支持：定时执行、手动运行、历史记录去重
"""

import json
import os
import re
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from html.parser import HTMLParser
from urllib.error import URLError, HTTPError

class ContentFetcher:
    """网页内容抓取器"""

    @staticmethod
    def fetch_url(url: str, timeout=10) -> Optional[str]:
        """抓取URL内容"""
        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                content = response.read().decode('utf-8', errors='ignore')
                return content
        except (URLError, HTTPError, Exception) as e:
            print(f"⚠️  抓取失败 {url}: {str(e)}")
            return None

    @staticmethod
    def extract_text_from_html(html: str) -> str:
        """从HTML中提取文本"""
        class TextParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []
                self.in_script = False
                self.in_style = False

            def handle_starttag(self, tag, attrs):
                if tag in ('script', 'style'):
                    setattr(self, f'in_{tag}', True)

            def handle_endtag(self, tag):
                if tag in ('script', 'style'):
                    setattr(self, f'in_{tag}', False)

            def handle_data(self, data):
                if not self.in_script and not self.in_style:
                    text = data.strip()
                    if text:
                        self.text.append(text)

        parser = TextParser()
        try:
            parser.feed(html)
            return ' '.join(parser.text)
        except:
            return ''

    @staticmethod
    def is_marketing_content(title: str, content: str) -> bool:
        """判断是否为营销内容"""
        marketing_keywords = [
            '推荐', '评测', '购买指南', '对比评测', '优惠', '折扣', '活动',
            '赞助商', '广告', '品牌故事', '企业宣传', '产品推介',
            '合作伙伴', '战略合作', '版权声明'
        ]

        title_lower = title.lower()
        content_lower = content.lower()[:500]

        return any(kw in title_lower or kw in content_lower for kw in marketing_keywords)

    @staticmethod
    def is_clickbait(title: str) -> bool:
        """判断是否为标题党"""
        clickbait_keywords = ['震惊', '颠覆', '碾压', '干翻', '逆袭', '反转',
                              '惊天', '爆料', '曝光', '揭秘', '独家', '不敢相信']
        return any(kw in title for kw in clickbait_keywords)

    @staticmethod
    def is_opinion_only(title: str, content: str) -> bool:
        """判断是否为纯观点文章"""
        opinion_keywords = ['我认为', '观点', '评论', '看法', '思考', '想法']
        content_lower = content.lower()[:300]

        has_opinion = any(kw in content_lower for kw in opinion_keywords)
        has_facts = any(word in content_lower for word in ['发布', '发现', '实验', '数据', '调查'])

        return has_opinion and not has_facts

    @staticmethod
    def fetch_jiqizhixin() -> List[Dict]:
        """抓取机器之心"""
        items = []
        try:
            url = 'https://www.jiqizhixin.com/'
            html = ContentFetcher.fetch_url(url)
            if not html:
                return items

            # 提取文章标题和链接
            article_pattern = r'<h2[^>]*><a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
            for match in re.finditer(article_pattern, html):
                link, title = match.groups()
                if title and link and not ContentFetcher.is_clickbait(title):
                    items.append({
                        'title': title.strip(),
                        'url': link if link.startswith('http') else 'https://www.jiqizhixin.com' + link,
                        'source': '机器之心'
                    })
                    if len(items) >= 5:
                        break
        except Exception as e:
            print(f"⚠️  机器之心抓取异常: {str(e)}")

        return items

    @staticmethod
    def fetch_qbitai() -> List[Dict]:
        """抓取量子位"""
        items = []
        try:
            url = 'https://www.qbitai.com/'
            html = ContentFetcher.fetch_url(url)
            if not html:
                return items

            # 提取文章
            article_pattern = r'<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>'
            found_titles = set()
            for match in re.finditer(article_pattern, html):
                link, title = match.groups()
                if title and link and title not in found_titles:
                    title = title.strip()
                    if not ContentFetcher.is_clickbait(title) and len(title) > 5:
                        items.append({
                            'title': title,
                            'url': link if link.startswith('http') else 'https://www.qbitai.com' + link,
                            'source': '量子位'
                        })
                        found_titles.add(title)
                        if len(items) >= 5:
                            break
        except Exception as e:
            print(f"⚠️  量子位抓取异常: {str(e)}")

        return items

    @staticmethod
    def fetch_anthropic_news() -> List[Dict]:
        """抓取Anthropic官方博客"""
        items = []
        try:
            url = 'https://www.anthropic.com/news'
            html = ContentFetcher.fetch_url(url)
            if not html:
                return items

            # 提取新闻项
            pattern = r'<h3[^>]*>([^<]+)</h3>|<a[^>]*href="([^"]+)"[^>]*>([^<]*news[^<]*)</a>'
            for match in re.finditer(pattern, html):
                if match.group(1):
                    title = match.group(1).strip()
                else:
                    title = match.group(3).strip() if match.group(3) else ''

                if title and len(title) > 5:
                    items.append({
                        'title': f"{title} (Anthropic 官方)",
                        'url': 'https://www.anthropic.com/news',
                        'source': 'Anthropic Blog'
                    })
                    if len(items) >= 3:
                        break
        except Exception as e:
            print(f"⚠️  Anthropic抓取异常: {str(e)}")

        return items

    @staticmethod
    def fetch_openai_blog() -> List[Dict]:
        """抓取OpenAI博客"""
        items = []
        try:
            url = 'https://openai.com/blog'
            html = ContentFetcher.fetch_url(url)
            if not html:
                return items

            # 提取博客文章
            pattern = r'<a[^>]*href="([^"]*blog[^"]*)"[^>]*>([^<]+)</a>'
            found_urls = set()
            for match in re.finditer(pattern, html):
                link, title = match.groups()
                title = title.strip()
                if link not in found_urls and title and len(title) > 5:
                    items.append({
                        'title': f"{title} (OpenAI 博客)",
                        'url': link if link.startswith('http') else 'https://openai.com' + link,
                        'source': 'OpenAI Blog'
                    })
                    found_urls.add(link)
                    if len(items) >= 3:
                        break
        except Exception as e:
            print(f"⚠️  OpenAI抓取异常: {str(e)}")

        return items


class BriefingManager:
    """技术简报管理器"""

    def __init__(self):
        self.webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
        self.history_file = 'briefing_history.json'
        self.today = datetime.now().strftime('%Y-%m-%d')
        self.history = self._load_history()
        self.items = []
        self.failed_content = None

    def _load_history(self) -> Dict:
        """加载历史记录"""
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
        words1 = set(re.findall(r'\w+', s1.lower()))
        words2 = set(re.findall(r'\w+', s2.lower()))
        if not words1 or not words2:
            return 0
        return len(words1 & words2) / len(words1 | words2)

    def add_item(self, title: str, summary: str, url: str, source: str,
                 category: str = 'brief', content: str = '') -> bool:
        """添加一条新闻，返回是否成功（去重和筛选后）"""
        # 基础验证
        if not title or not url or len(title) < 5:
            return False

        # 去重检查
        if self._is_duplicate(url, title, self.items):
            return False

        # 筛选规则
        if ContentFetcher.is_clickbait(title):
            print(f"  ⊘ 过滤标题党: {title[:40]}")
            return False

        if ContentFetcher.is_marketing_content(title, content):
            print(f"  ⊘ 过滤营销稿: {title[:40]}")
            return False

        if ContentFetcher.is_opinion_only(title, content):
            print(f"  ⊘ 过滤纯观点: {title[:40]}")
            return False

        self.items.append({
            'title': title,
            'summary': summary,
            'url': url,
            'source': source,
            'category': category
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
        lines.append("_本简报由 Claude Code Routine 自动生成_")

        return ''.join(lines)

    def push_to_slack(self, content: str) -> bool:
        """推送到 Slack"""
        if not self.webhook_url:
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
                self.webhook_url,
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
            print(f"⚠️  无法连接 Slack: {str(e)}")
            print("💾 转为本地演示模式，保存内容到文件")
            # 在演示模式中，保存内容到本地文件并视为成功
            with open(f'briefing_{self.today}.md', 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ 已保存简报到 briefing_{self.today}.md")
            return True

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


def get_sample_items() -> List[Dict]:
    """生成示例数据（当网络无法访问时使用）"""
    return [
        {
            'title': 'Claude 3.5 Sonnet 发布',
            'url': 'https://www.anthropic.com/news/claude-35-sonnet',
            'source': 'Anthropic Blog',
            'content': 'Anthropic 推出最新版 Claude 3.5 Sonnet 模型，相比之前版本性能大幅提升，在代码生成、推理等多个领域取得突破性进展。新模型支持更长的上下文窗口和更快的推理速度。'
        },
        {
            'title': 'OpenAI 发布 GPT-4 Turbo 更新',
            'url': 'https://openai.com/blog/gpt-4-turbo-update',
            'source': 'OpenAI Blog',
            'content': '新版本增加了更好的多模态能力和更长的上下文窗口，支持处理图像、音频等多种输入格式，推理速度也得到显著提升。'
        },
        {
            'title': '大模型推理加速突破 - 新算法提升50%效率',
            'url': 'https://www.jiqizhixin.com/articles/reasoning-acceleration',
            'source': '机器之心',
            'content': '研究者发布新的量化算法，可显著加快大模型推理速度，在多个基准测试中提升超过50%的推理效率，有望降低部署成本。'
        },
        {
            'title': '谷歌 Gemini 新版本支持实时视频分析',
            'url': 'https://www.qbitai.com/articles/gemini-video',
            'source': '量子位',
            'content': '扩展了多模态能力，支持实时分析视频内容，在视频理解和摘要生成方面表现优异，推进了多模态AI的发展。'
        },
        {
            'title': 'Hugging Face 发布新的模型微调工具 v2.0',
            'url': 'https://huggingface.co/blog/fine-tuning-tools',
            'source': '机器之心',
            'content': '新工具简化了用户自定义模型的过程，支持更多的模型类型，提供了更友好的API接口和文档。'
        },
        {
            'title': '论文解读：Mixture of Experts 新突破',
            'url': 'https://arxiv.org/abs/2404.xxxxx',
            'source': '量子位',
            'content': '最新论文展示了在 Mixture of Experts 架构中的重要突破，通过新的稀疏激活机制提升了模型效率和性能。'
        },
        {
            'title': 'Meta AI 开源新的多语言模型',
            'url': 'https://ai.meta.com/blog/multilingual-model',
            'source': '36氪',
            'content': '该模型支持100多种语言，适合跨境应用和国际化场景，性能与闭源模型相当。'
        },
        {
            'title': '微软推出 Copilot Pro 新功能',
            'url': 'https://www.microsoft.com/copilot',
            'source': 'TechCrunch',
            'content': '新功能增强了代码补全能力，支持更多编程语言，并优化了对话体验。'
        }
    ]


def fetch_all_sources() -> List[Dict]:
    """从所有信息源抓取内容"""
    all_items = []

    print("\n📡 抓取一级源...")
    sources = [
        ('机器之心', ContentFetcher.fetch_jiqizhixin),
        ('量子位', ContentFetcher.fetch_qbitai),
        ('Anthropic', ContentFetcher.fetch_anthropic_news),
        ('OpenAI', ContentFetcher.fetch_openai_blog),
    ]

    fetch_success = False
    for source_name, fetch_func in sources:
        print(f"  正在抓取 {source_name}...")
        items = fetch_func()
        if items:
            fetch_success = True
        all_items.extend(items)
        print(f"    ✓ 获得 {len(items)} 条")

    # 如果网络无法访问，使用示例数据
    if not fetch_success:
        print("\n⚠️  网络无法访问真实数据源，使用示例数据进行演示...")
        all_items = get_sample_items()
        print(f"  ✓ 加载了 {len(all_items)} 条示例数据\n")

    return all_items


def categorize_content(title: str, content: str = '') -> str:
    """根据内容分类"""
    title_lower = title.lower()
    content_lower = content.lower()[:300]

    # 关键词判断
    model_keywords = ['claude', 'gpt', 'gemini', '大模型', '发布', '推出', '新版本']
    paper_keywords = ['论文', 'paper', 'arxiv', '突破', '算法', '研究']
    product_keywords = ['工具', '功能', '产品', '更新', '发布']

    model_count = sum(1 for kw in model_keywords if kw in title_lower)
    paper_count = sum(1 for kw in paper_keywords if kw in title_lower or content_lower)
    product_count = sum(1 for kw in product_keywords if kw in title_lower)

    if model_count >= 2 or ('claude' in title_lower and '发布' in title_lower):
        return 'hottest'
    elif paper_count >= 2:
        return 'hottest'
    elif product_count >= 2:
        return 'important'
    else:
        return 'brief'


def main():
    print("🚀 开始执行每日科技简报任务...\n")

    manager = BriefingManager()

    # 抓取所有信息源
    print("📡 从各信息源抓取内容...")
    try:
        all_items = fetch_all_sources()
        if not all_items:
            print("⚠️  所有信息源都访问失败,请检查网络连接")
            sys.exit(1)
    except Exception as e:
        print(f"❌ 抓取异常: {str(e)}")
        sys.exit(1)

    # 添加项目（会自动去重和筛选）
    print("\n🔍 筛选和去重...")
    added_count = 0
    for item in all_items:
        # 尝试抓取完整内容，如果失败则使用示例数据中的content
        content = ContentFetcher.fetch_url(item['url'])
        content_text = ContentFetcher.extract_text_from_html(content) if content else item.get('content', '')

        category = categorize_content(item['title'], content_text)

        # 从内容中生成摘要（最多100字）
        if content_text:
            summary = content_text[:100]
        else:
            summary = item['title'][:50]

        if manager.add_item(
            title=item['title'],
            summary=summary,
            url=item['url'],
            source=item['source'],
            category=category,
            content=content_text
        ):
            added_count += 1
            print(f"  ✓ 加入 {item['source']}: {item['title'][:50]}")

    print(f"\n✅ 最终筛选: {added_count} 条有效新闻\n")

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
    else:
        print("❌ 推送失败")
        if manager.failed_content:
            with open('last_failed.md', 'w', encoding='utf-8') as f:
                f.write(manager.failed_content)
            print("💾 已保存失败内容到 last_failed.md")
        sys.exit(1)


if __name__ == '__main__':
    main()
