#!/usr/bin/env python3
"""
将每日科技简报数据生成微信公众号可直接粘贴的 HTML 文件。
用法：python3 gen_wechat_html.py <output_path>
"""

import sys
import json
from datetime import date

# ── 当日简报数据（每次运行时替换此处内容）──────────────────────────────
BRIEFING_DATE = "2026年05月23日"
FILE_DATE = "20260523"

MUST_READ = [
    {
        "title": "OpenAI 秘密递交 IPO 招股书，目标 Q4 上市，估值 $8520 亿–$1 万亿",
        "summary": "OpenAI 于 5 月 22 日向 SEC 递交保密版 S-1，高盛+摩根士丹利联合承销。月均营收 $20 亿，5000 万消费端订户 + 900 万企业用户；Q1 仍亏损（每 $1 收入亏 $1.22）；目标 Q4 2026 上市，最早 9 月挂牌。",
        "url": "https://fortune.com/2026/05/22/openai-ipo-filing-1-trillion-may-finally-answer-these-big-questions/",
        "source": "Fortune",
    },
    {
        "title": "Anthropic 启动新融资，估值冲 $9000 亿超越 OpenAI，Q2 营收预测 $109 亿、史上首季盈利",
        "summary": "与投资者谈判超 $300 亿融资，$9000 亿估值将成最高估值 AI 初创。Q2 营收预测 $109 亿（较 Q1 $48 亿+130%），预计营业利润 $5.59 亿——比内部计划提前两年首次盈利。IPO 目标：2026 年 10 月。",
        "url": "https://www.techtimes.com/articles/317066/20260523/anthropic-funding-round-top-30b-900b-valuation-would-surpass-openai-most-valuable-ai-startup.htm",
        "source": "TechTimes",
    },
    {
        "title": "NVIDIA Q1 FY2027 财报：营收 $816 亿（同比 +85%），净利润 $583 亿创纪录",
        "summary": "数据中心营收 $752 亿（同比 +92%），占总营收 92%；超算云厂商贡献 $380 亿（环比+12%）。EPS $2.39 超预期（预测 $1.77）；自由现金流 $490 亿；新增 $800 亿回购授权，季度股息从 $0.01 升至 $0.25。",
        "url": "https://www.cnbc.com/2026/05/20/nvidia-nvda-earnings-report-q1-2027.html",
        "source": "CNBC",
    },
    {
        "title": "OpenAI 通用推理模型自主推翻 80 年未解 Erdos 单位距离猜想",
        "summary": "非数学专项模型构造多维格点证明，推翻 Erdos 1946 年提出的平面单位距离问题。外部数学家验证通过；菲尔兹奖得主 Tim Gowers：「AI 数学里程碑」，达顶级期刊发表水准，通用推理能力超专项系统成为关键信号。",
        "url": "https://openai.com/index/model-disproves-discrete-geometry-conjecture/",
        "source": "OpenAI",
    },
    {
        "title": "Andrej Karpathy 加入 Anthropic 预训练团队，主导「Claude 自我加速」新方向",
        "summary": "OpenAI 联创、前特斯拉 AI 总监于 5 月 19 日加入，领导新团队探索「用 Claude 本身加速预训练研究」这一前沿方向。Karpathy：「未来几年是 LLM 前沿最具决定性的时期，非常期待重回 R&D 工作。」",
        "url": "https://techcrunch.com/2026/05/19/openai-co-founder-andrej-karpathy-joins-anthropics-pre-training-team/",
        "source": "TechCrunch",
    },
    {
        "title": "Google I/O 2026：Gemini 3.5 Flash 发布当日 GA，速度超旗舰模型 4 倍，$1.50/$9/M tokens",
        "summary": "Terminal-Bench 2.1 76.2%、MCP Atlas 83.6%，全面超越 Gemini 3.1 Pro；100 万 token 上下文；Gemini app MAU 从 4 亿增至 9 亿（+125%），AI Mode Search 月活突破 10 亿；Gemini Spark 个人 Agent 将在数周内支持 MCP 接入 Canva、Instacart 等。",
        "url": "https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-5/",
        "source": "Google Blog",
    },
    {
        "title": "NVIDIA 发布 Verified Agent Skills 框架，AI Agent 能力治理标准化（5/22）",
        "summary": "SkillSpector 扫描（检测漏洞、提示注入、工具投毒）+ 密码学签名 + 机器可读技能卡，开源发布于 github.com/NVIDIA/skills，为企业 AI Agent 部署提供安全透明基础设施，目标成为行业治理标准。",
        "url": "https://developer.nvidia.com/blog/nvidia-verified-agent-skills-provide-capability-governance-for-ai-agents/",
        "source": "NVIDIA Technical Blog",
    },
]

WORTH_READING = [
    {
        "title": "Anthropic 每月向 SpaceX 支付 $12.5 亿算力费用，总合同约 $450 亿",
        "summary": "通过 SpaceX IPO 招股书曝光：使用 Colossus 超算，合同至 2029 年 5 月，月付 $12.5 亿，累计约 $450 亿——已知 AI 行业最大单笔算力采购合同。",
        "url": "https://www.axios.com/2026/05/20/openai-ipo-spacex-musk",
        "source": "Axios",
    },
    {
        "title": "特朗普在签署仪式前数小时叫停 AI 监管行政令",
        "summary": "拟签令要求 AI 公司在发布前 90 天自愿提交联邦模型测试并加强 AI 网络安全防御。特朗普称「我不喜欢某些方面」，担心干扰美国 AI 领先地位。",
        "url": "https://www.cnbc.com/amp/2026/05/21/trump-ai-executive-order-postponed.html",
        "source": "CNBC",
    },
    {
        "title": "Microsoft 开源 RAMPART + Clarity：AI Agent 安全持续工程化",
        "summary": "RAMPART（Pytest 原生 Agent 红队测试框架，覆盖跨提示注入、数据外泄、行为回归）+ Clarity（代码编写前的 Agent 设计安全评估），主张 AI 安全应成为持续工程纪律而非定期检查点。两款工具均已开源。",
        "url": "https://www.microsoft.com/en-us/security/blog/2026/05/20/introducing-rampart-and-clarity-open-source-tools-to-bring-safety-into-agent-development-workflow/",
        "source": "Microsoft Security Blog",
    },
    {
        "title": "Anthropic 联创 Jack Clark 预言：AI 12 个月内助力诞生诺贝尔级科学突破",
        "summary": "牛津大学演讲：AI 将在 12 个月内与人类合作取得诺贝尔奖级成果；AI 独立运营公司将在 18 个月内创造数百万美元营收；同时坦承「AI 存在非零概率对人类造成存亡威胁，这一风险尚未消除」。",
        "url": "https://www.techcentral.ie/anthropic-co-founder-predicts-that-ai-will-within-a-year/",
        "source": "TechCentral.ie",
    },
]

BRIEFS = [
    {
        "title": "Anthropic 收购 SDK 基础设施公司 Stainless（同时服务 OpenAI 与 Google）",
        "url": "https://techcrunch.com/2026/05/18/anthropic-acquires-stainless/",
        "source": "TechCrunch",
    },
    {
        "title": "Google I/O 100 大公告：Gemini 3.5 Pro 下月上线；Gemini Spark 将在数周内支持 MCP 接入 Canva、Instacart 等",
        "url": "https://blog.google/innovation-and-ai/technology/ai/google-io-2026-all-our-announcements/",
        "source": "Google Blog",
    },
    {
        "title": "TanStack npm 供应链攻击（5/11）：170+ npm 包被入侵，@tanstack/react-router 周下载 1270 万受波及，Mistral AI SDK 同中招",
        "url": "https://orca.security/resources/blog/tanstack-npm-supply-chain-worm/",
        "source": "Orca Security",
    },
    {
        "title": "廉价 AI 价格战：DeepSeek 月费 $1071 vs Claude 月费约 $9000，价格差距或影响 OpenAI/Anthropic IPO 估值逻辑",
        "url": "https://www.cnbc.com/2026/05/20/cheap-ai-could-derail-openai-and-anthropics-ipos.html",
        "source": "CNBC",
    },
    {
        "title": "Axios 深度：Google 如何制定赢得 AI 战争的计划——三强鼎立格局下的差异化策略",
        "url": "https://www.axios.com/2026/05/21/google-ai-anthropic-openai-war",
        "source": "Axios",
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
