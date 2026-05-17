#!/usr/bin/env python3
"""
将每日科技简报数据生成微信公众号可直接粘贴的 HTML 文件。
用法：python3 gen_wechat_html.py <output_path>
"""

import sys
import json
from datetime import date

# ── 当日简报数据（每次运行时替换此处内容）──────────────────────────────
BRIEFING_DATE = "2026年05月16日"
FILE_DATE = "20260516"

MUST_READ = [
    {
        "title": "OpenAI ChatGPT 推出个人理财功能：连接 12,000+ 银行账户，GPT-5.5 驱动财务问答",
        "summary": "ChatGPT 向美国 Pro 用户开放 Finances 功能，通过 Plaid 接入 12,000+ 金融机构，提供资产仪表盘（消费/订阅/投资/净资产全景），支持跨对话「财务记忆」。GPT-5.5 负责复杂财务推理；可读取余额和交易记录，不可操作账户。先向 Pro 小规模开放，后续扩展至 Plus 和免费用户。",
        "url": "https://openai.com/index/personal-finance-chatgpt/",
        "source": "OpenAI 官方",
    },
    {
        "title": "Google I/O 三天倒计时：Gemini 3.2 Flash + Gemini Omni 双双泄露",
        "summary": "Gemini 3.2 Flash 悄然现身 iOS App 和 AI Studio：响应 <200ms，定价 $0.25/$2.00 per M tokens（远低于 3.1 Pro），知识截止日更新至 2026 年 1 月，编码能力接近 3.1 Pro。同期「Gemini Omni」字符串出现在视频生成标签，暗示文本/图像/视频三合一管道。主题演讲 5 月 19 日 10AM PT 全部揭晓。",
        "url": "https://nokiapoweruser.com/gemini-3-2-flash-leak-fast-cheap-ai-google-io-2026/",
        "source": "Nokia Power User / AIxploria",
    },
    {
        "title": "Musk v. Altman：陪审团开始审议，建议性裁决与 OpenAI 万亿 IPO 悬念同步",
        "summary": "三周庭审落幕，9 人陪审团（6 女 3 男）开始审议，裁决为「建议性」，法官 Gonzalez Rogers 最终拍板。Musk 方：Ilya Sutskever 等 5 位证人指证 Altman 说谎，诉求 $1,500 亿赔偿 + Altman 出局 + 撤销商业化改组。Musk 本人结案陈词时在北京陪特朗普访华。若法官判 Musk 胜，OpenAI 约 $1 万亿 IPO 进程或受阻。",
        "url": "https://localnewsmatters.org/2026/05/16/musk-v-altman-week-3-analysis-jurors-face-tangled-questions-of-trust-timing-and-ai/",
        "source": "Local News Matters / Washington Post",
    },
    {
        "title": "Samsung 5 万芯片工人 5/21 启动 18 天罢工：$34 万奖金被拒，要求 $90 万年度分红",
        "summary": "工人拒绝一次性 $34 万美元奖金方案，对标 SK 海力士约 $90 万年度分红。JPMorgan 估算：18 天罢工令三星营业利润损失 $140 亿至 $208 亿。HBM、DRAM 全球 AI 数据中心内存价格面临上行压力。工会称 6 月 7 日罢工结束后再谈，管理层提议无条件恢复谈判。",
        "url": "https://www.tomshardware.com/tech-industry/big-tech/samsung-chip-workers-reject-usd340-000-one-time-bonus-demand-annual-payouts-like-sk-hynixs-usd900-000-workers-want-share-of-ai-windfall-impending-18-day-strike-could-cost-samsung-up-to-usd11-7-billion",
        "source": "Tom's Hardware",
    },
]

WORTH_READING = [
    {
        "title": "Anthropic + Gates Foundation 签署 $2 亿 AI 合作：聚焦全球健康、教育与农业",
        "summary": "4 年内共投 $2 亿（含资金、Claude 用量积分和技术支持），聚焦低中收入国家医疗（脊髓灰质炎/HPV/子痫前期），以及美国和非洲/印度的 K-12 教育辅导。Anthropic 将改进 Claude 对数十种非洲语言的理解，并公开发布数据集。",
        "url": "https://www.anthropic.com/news/gates-foundation-partnership",
        "source": "Anthropic 官方",
    },
    {
        "title": "GitHub Copilot Agent 模式在 Visual Studio 正式 GA + v1.0.48 定价透明化",
        "summary": "Agent 模式支持单提示规划并执行多步骤编码任务，可跨文件推理、迭代修复错误直到目标完成。v1.0.48：模型选择器改为显示实际 token 价格（取代圆点），开发者可直观比较模型成本。",
        "url": "https://www.havoptic.com/tools/github-copilot",
        "source": "Havoptic Changelog",
    },
    {
        "title": "Recursive Superintelligence 以 $4.65B 估值携 $6.5 亿出山，押注 AI 无监督自我改进",
        "summary": "Richard Socher（前 Salesforce 首席科学家）+ UCL 教授 Tim Rocktäschel 创立，GV（Google VC）+ Greycroft 领投，Nvidia、AMD 参投。团队不足 30 人，核心赌注：AI 通过分析自身表现实现无人工干预的持续进化，2026 年中公开发布。",
        "url": "https://thenextweb.com/news/recursive-superintelligence-self-improving-ai-funding",
        "source": "The Next Web",
    },
    {
        "title": "Mira Murati 的 Thinking Machines 发布「交互模型」：0.4 秒响应、276B MoE 全双工",
        "summary": "TML-Interaction-Small 是 276B 参数 MoE 模型（同时激活 12B），实现 200ms 微回合替代传统「请求-响应」循环；全双工——AI 可同时说话、倾听并调用工具。响应延迟 0.4 秒，限量研究预览，对标 OpenAI Realtime API。",
        "url": "https://www.marktechpost.com/2026/05/13/mira-muratis-thinking-machines-lab-introduces-interaction-models-a-native-multimodal-architecture-for-real-time-human-ai-collaboration/",
        "source": "MarkTechPost",
    },
]

BRIEFS = [
    {
        "title": "Musk v. Altman 庭审分析：Musk 诚信为何成为攻防焦点",
        "url": "https://www.washingtonpost.com/technology/2026/05/16/elon-musk-trial-against-sam-altman-renews-questions-about-his-honesty/",
        "source": "Washington Post",
    },
    {
        "title": "Samsung 罢工背后：AI 芯片繁荣如何撕裂内部薪酬体系",
        "url": "https://www.malaymail.com/amp/news/money/2026/05/16/how-samsungs-ai-chip-success-has-led-workers-to-threaten-its-biggest-ever-strike/220166",
        "source": "Malay Mail",
    },
    {
        "title": "Gemini Omni 全泄露梳理：Google 统一视频/图像/文本生成管道技术细节",
        "url": "https://lovegen.ai/blog/gemini-omni-leak-google-io-2026",
        "source": "LoveGen AI",
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
