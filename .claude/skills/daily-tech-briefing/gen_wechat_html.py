#!/usr/bin/env python3
"""
将每日科技简报数据生成微信公众号可直接粘贴的 HTML 文件。
用法：python3 gen_wechat_html.py <output_path>
"""

import sys
import json
from datetime import date

# ── 当日简报数据（每次运行时替换此处内容）──────────────────────────────
BRIEFING_DATE = "2026年05月15日"
FILE_DATE = "20260515"

MUST_READ = [
    {
        "title": "Anthropic 商业采用率历史首次超越 OpenAI",
        "summary": "Ramp AI Index 4月数据：美国商业客户中 Claude 付费采用率达 34.4%（较上月 +3.8%），首次超过 OpenAI 32.3%（-2.9%）。Anthropic 一年内从 7.94% 飙升至 34.44%；Claude Code 占全球 GitHub 公开 commits 的 4%（较上月翻倍），成为 Anthropic 史上增长最快产品。",
        "url": "https://venturebeat.com/technology/anthropic-finally-beat-openai-in-business-ai-adoption-but-3-big-threats-could-erase-its-lead",
        "source": "VentureBeat / Ramp",
    },
    {
        "title": "Salesforce Summer '26 发布：Agentforce ARR 破 8 亿美元（+169% YoY），Tableau MCP 首推",
        "summary": "Summer '26（6月15日上线）核心亮点：多智能体编排（Multi-Agent Orchestration）、Tableau MCP（Agent 直查 Tableau 分析引擎）、Slack First Sales、Agentforce Operations（后台工作流 Agent 化）；Agentforce ARR 8亿美元（+169%），AI 总 ARR 29亿美元。Tableau MCP 是首个将主流 BI 引擎纳入 MCP 生态的成熟方案。",
        "url": "https://www.salesforce.com/news/stories/summer-2026-product-release-announcement/",
        "source": "Salesforce",
    },
    {
        "title": "Trump-Xi 北京峰会收官：H200 出口框架成形，特朗普邀 Xi 9月24日访白宫",
        "summary": "两天峰会（5/14-15）正式结束，白宫定性「进展良好」；H200 对 10 家中国科技公司出口框架基本落地，预计恢复 Nvidia 年度约 35-40 亿美元中国营收；90天关税休战（美方 145%→30%，中方 125%→10%）继续维持；特朗普邀习近平 9月24日访问白宫。",
        "url": "https://www.gmanetwork.com/news/topstories/world/987610/trump-visit-china-xi-jinping-trade-talks-taiwan/story/",
        "source": "GMA News / CNBC",
    },
    {
        "title": "Musk v. Altman：结案陈词完毕，陪审团今日开始商议",
        "summary": "陪审团 5/15 开始商议，裁决周内可期。Musk 律师指控 Altman 以股权自肥违反非营利使命；OpenAI 律师以 Shivon Zilis 证词反击；Ilya Sutskever 庭上披露持有约 70 亿美元 OpenAI 股权。若 Altman 被裁定违反信托义务，OpenAI 非营利转型合法性将受冲击。",
        "url": "https://abc7news.com/live-updates/elon-musk-sam-altman-live-updates-microsoft-ceo-satya-nadella-testify-week-3-trial-begins/19080697/",
        "source": "ABC7",
    },
    {
        "title": "xAI Grok 4.3：今日 8 款旧版模型强制退役（12:00 PM PT）",
        "summary": "grok-3、grok-4-0709、grok-4-1-fast-reasoning、grok-code-fast-1 等 8 款模型今日正式停服，API 请求自动重定向至 grok-4.3（$1.25/$2.50 per 1M tokens）；未主动迁移仍使用旧 slug 但立即按新价格计费。grok-4.3 支持 1M token 上下文、3 档可调推理强度。",
        "url": "https://docs.x.ai/developers/migration/may-15-retirement",
        "source": "xAI Docs",
    },
]

WORTH_READING = [
    {
        "title": "Salesforce Agentforce Operations：后台工作流全 Agent 化，对标 ServiceNow",
        "summary": "Salesforce 独立发布 Agentforce Operations，将企业后台流程（订单处理、财务对账等）分解为 Agent 任务图，由专属 Agent 并行处理，附 Blueprint 模板库降低落地门槛。与 Summer '26 同日发布，竞争 ServiceNow 工作流自动化市场。",
        "url": "https://venturebeat.com/orchestration/salesforce-launches-agentforce-operations-to-fix-the-workflows-breaking-enterprise-ai",
        "source": "VentureBeat",
    },
    {
        "title": "Cloudflare Project Think：为 AI Agent 打造边缘推理基础设施",
        "summary": "推出 Infire 推理引擎（跨多 GPU 分布运行大模型）和 Unweight 权重压缩（节省 15-22% 推理带宽）；已托管 Moonshot Kimi K2.5 并实现 3× 提速，更多开源模型接入中。目标：让 AI Agent 在 Cloudflare 全球边缘节点稳定执行，竞争 AWS/GCP 推理服务市场。",
        "url": "https://blog.cloudflare.com/project-think/",
        "source": "Cloudflare Blog",
    },
]

BRIEFS = [
    {
        "title": "Google DeepMind Magic Pointer：Gemini 驱动智能鼠标，即将集成 Chrome",
        "url": "https://9to5google.com/2026/05/12/deepmind-googlebook-magic-pointer/",
        "source": "9to5Google",
    },
    {
        "title": "Trump-Xi 峰会推动中国 AI 科技股大涨，腾讯/阿里等美股盘前劲升",
        "url": "https://www.cnbc.com/2026/05/14/trump-xi-meeting-china-stocks-ai-rally.html",
        "source": "CNBC",
    },
    {
        "title": "Ramp AI Index 完整报告：过去一年 Anthropic 商业采用率增幅达 327%，OpenAI 仅增 0.3%",
        "url": "https://ramp.com/leading-indicators/ai-index-may-2026",
        "source": "Ramp",
    },
]
# ────────────────────────────────────────────────────────────────────────────


def render_html(date_str, must_read, worth_reading, briefs):
    def item_block(idx, item, show_summary=True):
        summary_html = (
            f'<p style="margin:6px 0 12px 0;color:#444;font-size:15px;line-height:1.7;">'
            f'{item["summary"]}</p>'
        ) if show_summary and item.get("summary") else ""
        return (
            f'<p style="margin:14px 0 4px 0;">'
            f'<strong style="font-size:16px;">{idx}. {item["title"]}</strong>'
            f'</p>'
            f'{summary_html}'
            f'<p style="margin:0 0 20px 0;font-size:14px;">'
            f'<a href="{item["url"]}" style="color:#576b95;text-decoration:none;">阅读原文</a>'
            f'&nbsp;&nbsp;<span style="color:#999;">· {item["source"]}</span>'
            f'</p>'
        )

    must_html = "".join(item_block(i + 1, it) for i, it in enumerate(must_read))
    worth_html = "".join(item_block(i + 1, it) for i, it in enumerate(worth_reading))
    brief_html = "".join(
        f'<p style="margin:4px 0;font-size:14px;">'
        f'<a href="{it["url"]}" style="color:#576b95;text-decoration:none;">{it["title"]}</a>'
        f'&nbsp;<span style="color:#999;">· {it["source"]}</span>'
        f'</p>'
        for it in briefs
    )

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>AI 简报 | {date_str}</title>
</head>
<body style="max-width:680px;margin:40px auto;font-family:'PingFang SC','Helvetica Neue',Arial,sans-serif;color:#222;">

<h1 style="font-size:22px;font-weight:bold;border-bottom:2px solid #333;padding-bottom:10px;margin-bottom:24px;">
  AI 简报 | {date_str}
</h1>

<h2 style="font-size:17px;margin:28px 0 12px 0;padding:6px 12px;background:#f5f5f5;border-left:4px solid #333;">
  必读
</h2>
{must_html}

<h2 style="font-size:17px;margin:28px 0 12px 0;padding:6px 12px;background:#f5f5f5;border-left:4px solid #333;">
  值得看
</h2>
{worth_html}

<h2 style="font-size:17px;margin:28px 0 12px 0;padding:6px 12px;background:#f5f5f5;border-left:4px solid #333;">
  简讯
</h2>
{brief_html}

<p style="margin-top:40px;font-size:13px;color:#aaa;border-top:1px solid #eee;padding-top:12px;">
  每日 AI 科技简报，由 Claude Code 自动整理发布。
</p>

</body>
</html>"""


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else f"news/2026-05/{FILE_DATE}.html"
    html = render_html(BRIEFING_DATE, MUST_READ, WORTH_READING, BRIEFS)
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"✅ 生成完成：{out}")
    print("   在浏览器中打开 → 全选(Ctrl+A) → 复制(Ctrl+C) → 粘贴到公众号编辑器")
