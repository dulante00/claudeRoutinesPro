#!/usr/bin/env python3
"""
将每日科技简报数据生成微信公众号可直接粘贴的 HTML 文件。
用法：python3 gen_wechat_html.py <output_path>
"""

import sys
import json
from datetime import date

# ── 当日简报数据（每次运行时替换此处内容）──────────────────────────────
BRIEFING_DATE = "2026年05月14日"
FILE_DATE = "20260514"

MUST_READ = [
    {
        "title": "美国批准向10家中国科技公司出售 Nvidia H200，附25%收入分成，但北京叫停下单",
        "summary": "阿里、腾讯、字节、京东等获批每家最多75,000颗 H200，须经美国境内中转并缴纳25%收入分成；然而北京指示企业暂缓下单，转而扶植华为自主芯片，实际出货量为零。",
        "url": "https://www.cnbc.com/2026/05/14/us-clears-h200-chip-sales-to-10-china-firms-as-nvidia-ceo-looks-for-breakthrough.html",
        "source": "CNBC",
    },
    {
        "title": "Anthropic 拟以 $3 亿+ 收购 SDK 创企 Stainless（同时服务 OpenAI 与 Google）",
        "summary": "Stainless 为 Anthropic、OpenAI、Google 三家生成多语言 SDK 及 MCP 服务器；收购完成后 Anthropic 将掌控竞争对手的开发者接入层，条款仍在磋商，未签意向书。",
        "url": "https://winbuzzer.com/2026/05/14/anthropic-in-talks-to-buy-developer-tools-startup-xcxwbn/",
        "source": "The Information",
    },
    {
        "title": "Musk v. Altman 进入结案陈词：Musk 出访中国，律师代为出席道歉",
        "summary": "Musk 律师向陪审团道歉客户缺席庭审，结案陈词当日完成。Musk 方索赔最高 $1500 亿并要求解除 Altman/Brockman 职务；最终判决权归 Yvonne Gonzalez Rogers 法官，结果近期公布。",
        "url": "https://www.axios.com/2026/05/14/musk-closing-arguments-openai-altman",
        "source": "Axios",
    },
]

WORTH_READING = [
    {
        "title": "习近平会见马斯克、库克等随行美国科技 CEO：中国大门只会越开越大",
        "summary": "随行代表团包括马斯克、黄仁勋、库克等，习近平明确欢迎美企加深对华合作，AI 与芯片领域具体条款预计峰会后落地。",
        "url": "https://www.cnbc.com/2026/05/14/xi-china-open-us-business-ai-chips.html",
        "source": "CNBC",
    },
    {
        "title": "前阿里 Qwen 负责人林俊旸创业：世界模型 + 具身 AI，首轮估值约 $20 亿",
        "summary": "32岁前阿里最年轻 P10 技术负责人、Qwen 系列主要负责人林俊旸为新 AI 实验室融资，首轮融后估值约 $20 亿（约人民币 136 亿），高榕资本和红杉中国洽谈参与。",
        "url": "https://www.qbitai.com/2026/05/416963.html",
        "source": "量子位",
    },
    {
        "title": "百度 Create 2026：李彦宏提出以 DAA（日活智能体数）取代 Token 消耗衡量 AI 平台价值",
        "summary": "李彦宏主张智能体时代应以「日活智能体数」（Daily Active Agents）而非 Token 消耗衡量平台价值，关注实际运行并交付结果的 Agent 数量，千帆 3.0 同期亮相。",
        "url": "https://finance.sina.com.cn/tech/digi/2026-05-13/doc-inhxtkrt4626639.shtml",
        "source": "新浪财经",
    },
]

BRIEFS = [
    {
        "title": "AI 开发者用 OpenAI Codex + Claude 5周复刻 RAR 压缩算法，生成5.5万行代码",
        "url": "https://www.80aj.com/2026/05/14/ai-rar-compression-llm/",
        "source": "80aj.com",
    },
    {
        "title": "H200 获批零出货：北京叫停下单，华为自主芯片路线成关键变量",
        "url": "https://thenextweb.com/news/nvidia-h200-china-licences-huang-beijing-trip",
        "source": "The Next Web",
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
