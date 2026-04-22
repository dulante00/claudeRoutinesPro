#!/usr/bin/env python3
"""
从各个信息源抓取科技新闻的脚本
支持: 机器之心、量子位、36氪、Hacker News等
"""

import json
import re
import subprocess
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from typing import List, Dict
import html

USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

class NewsSource:
    """新闻源基类"""

    def __init__(self, name: str, url: str, priority: int = 3):
        self.name = name
        self.url = url
        self.priority = priority  # 1=必查, 2=有余力, 3=深度补充
        self.articles = []

    def fetch(self) -> List[Dict]:
        """抓取新闻，返回文章列表"""
        raise NotImplementedError

    def is_recent(self, pub_date_str: str) -> bool:
        """检查是否在过去24小时内发布"""
        if not pub_date_str:
            return False

        try:
            # 尝试多种日期格式
            for fmt in ['%Y-%m-%d %H:%M:%S', '%Y-%m-%d', '%Y-%m-%dT%H:%M:%S', '%d/%m/%Y']:
                try:
                    pub_date = datetime.strptime(pub_date_str, fmt)
                    break
                except ValueError:
                    continue
            else:
                # 尝试提取日期部分
                date_match = re.search(r'(\d{4})-(\d{1,2})-(\d{1,2})', pub_date_str)
                if date_match:
                    pub_date = datetime.strptime(f"{date_match.group(1)}-{date_match.group(2)}-{date_match.group(3)}", '%Y-%m-%d')
                else:
                    return False

            cutoff = datetime.now() - timedelta(hours=24)
            return pub_date > cutoff
        except Exception:
            return False

    @staticmethod
    def fetch_url(url: str) -> str:
        """通过Python简单爬虫获取页面内容"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': USER_AGENT})
            with urllib.request.urlopen(req, timeout=10) as response:
                return response.read().decode('utf-8', errors='ignore')
        except Exception as e:
            print(f"❌ 获取 {url} 失败: {e}")
            return ""

    @staticmethod
    def extract_text(html_str: str, tag: str = 'p') -> str:
        """从HTML提取文本"""
        pattern = f'<{tag}[^>]*>([^<]*)</{tag}>'
        matches = re.findall(pattern, html_str, re.IGNORECASE)
        text = ' '.join(matches)
        return html.unescape(text)[:100]  # 只取前100字

class JiQiZhiXin(NewsSource):
    """机器之心 (jiqizhixin.com)"""

    def __init__(self):
        super().__init__('机器之心', 'https://www.jiqizhixin.com/', priority=1)

    def fetch(self) -> List[Dict]:
        """抓取机器之心的新闻"""
        articles = []
        try:
            html = self.fetch_url(self.url)
            if not html:
                return articles

            # 提取新闻链接和标题
            # 机器之心的结构: <a href="/article/..." title="...">...</a>
            pattern = r'<a\s+href=["\'](/article/[^"\']*)["\'][^>]*title=["\']([^"\']*)["\']'
            matches = re.findall(pattern, html)

            for url_path, title in matches[:10]:  # 只取前10条
                full_url = f"https://www.jiqizhixin.com{url_path}"
                # 提取文章摘要（这里简化处理）
                summary = self.extract_summary(title)

                if self._is_relevant(title):
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'url': full_url,
                        'source': self.name,
                        'priority': self.priority
                    })

        except Exception as e:
            print(f"❌ 机器之心抓取失败: {e}")

        return articles

    def _is_relevant(self, title: str) -> bool:
        """检查标题是否相关（LLM/AI/科技）"""
        keywords = ['LLM', 'AI', 'Claude', 'GPT', 'Gemini', 'DeepSeek', '大模型', '模型', '算法', '深度学习',
                    '机器学习', '神经网络', '自然语言', '生成式', '人工智能']
        title_lower = title.lower()
        return any(keyword.lower() in title_lower for keyword in keywords)

    @staticmethod
    def extract_summary(title: str) -> str:
        """从标题提取摘要"""
        # 这里可以做更复杂的处理，目前简化返回标题本身
        return title[:80]

class QBit(NewsSource):
    """量子位 (qbitai.com)"""

    def __init__(self):
        super().__init__('量子位', 'https://www.qbitai.com/', priority=1)

    def fetch(self) -> List[Dict]:
        """抓取量子位的新闻"""
        articles = []
        try:
            html = self.fetch_url(self.url)
            if not html:
                return articles

            # 提取新闻链接
            pattern = r'<a\s+href=["\']([^"\']*)["\'][^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html)

            for url, title in matches[:10]:
                if 'article' in url and self._is_relevant(title):
                    summary = title[:80]
                    articles.append({
                        'title': title,
                        'summary': summary,
                        'url': url if url.startswith('http') else f"https://www.qbitai.com{url}",
                        'source': self.name,
                        'priority': self.priority
                    })

        except Exception as e:
            print(f"❌ 量子位抓取失败: {e}")

        return articles

    @staticmethod
    def _is_relevant(title: str) -> bool:
        """检查标题是否相关"""
        keywords = ['LLM', 'AI', 'Claude', 'GPT', 'Gemini', '大模型', '模型', '算法']
        return any(keyword.lower() in title.lower() for keyword in keywords)

class HackerNews(NewsSource):
    """Hacker News (news.ycombinator.com)"""

    def __init__(self):
        super().__init__('Hacker News', 'https://news.ycombinator.com/', priority=2)

    def fetch(self) -> List[Dict]:
        """抓取Hacker News的AI相关新闻"""
        articles = []
        try:
            html = self.fetch_url(self.url)
            if not html:
                return articles

            # 提取新闻标题和链接
            pattern = r'<span class="titleline"><a[^>]*href="([^"]*)"[^>]*>([^<]+)</a>'
            matches = re.findall(pattern, html)

            for url, title in matches[:15]:
                if any(kw in title.lower() for kw in ['llm', 'ai', 'claude', 'gpt', 'ml', 'neural']):
                    articles.append({
                        'title': f"{title} (Hacker News)",
                        'summary': title[:80],
                        'url': url if url.startswith('http') else f"https://news.ycombinator.com/{url}",
                        'source': self.name,
                        'priority': self.priority
                    })

        except Exception as e:
            print(f"❌ Hacker News抓取失败: {e}")

        return articles

def main():
    """运行所有源的抓取"""
    sources = [
        JiQiZhiXin(),
        QBit(),
        HackerNews(),
    ]

    all_articles = []

    print("📡 开始从多个信息源抓取新闻...\n")

    for source in sources:
        print(f"🔄 正在从 {source.name} 抓取...")
        try:
            articles = source.fetch()
            all_articles.extend(articles)
            print(f"✅ {source.name}: 获取 {len(articles)} 条新闻\n")
        except Exception as e:
            print(f"❌ {source.name} 抓取失败: {e}\n")

    # 输出结果
    if all_articles:
        print(f"\n{'='*50}")
        print(f"📊 抓取完成，共获得 {len(all_articles)} 条新闻")
        print(f"{'='*50}\n")
        print("样本新闻:")
        for i, article in enumerate(all_articles[:5], 1):
            print(f"{i}. {article['title']}")
            print(f"   来源: {article['source']}")
            print(f"   链接: {article['url']}\n")
    else:
        print("❌ 未能获取任何新闻")

    # 保存到JSON用于后续处理
    with open('temp_articles.json', 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    return all_articles

if __name__ == '__main__':
    main()
