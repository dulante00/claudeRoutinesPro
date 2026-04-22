---
name: daily-tech-briefing
description: 每日 LLM 与科技新闻简报,抓取、筛选、整理成中文摘要并通过 Slack Connector 推送到 Slack
---

# 每日 LLM 与科技新闻简报

## 任务目标

每天早上生成一份简洁的中文科技新闻简报,通过 Slack Connector 推送到 Slack 频道。
内容聚焦 LLM、AI、前沿科技,过滤营销和水文。

---

## 信息源(按优先级从高到低)

### 一级源(必查)
- **机器之心** https://www.jiqizhixin.com/
- **量子位** https://www.qbitai.com/
- **Anthropic 官方博客** https://www.anthropic.com/news (英文,翻译成中文)
- **OpenAI Blog** https://openai.com/blog (英文,翻译成中文)

### 二级源(有余力就查)
- **36氪 AI 频道** https://36kr.com/information/AI/
- **InfoQ 中文** https://www.infoq.cn/topic/AI
- **少数派** https://sspai.com/ (科技类)
- **Hacker News** https://news.ycombinator.com/ (挑 AI/LLM 相关的,用中文总结)

### 三级源(深度补充)
- **arXiv cs.CL** https://arxiv.org/list/cs.CL/recent (挑当天 Top 讨论论文)

---

## 筛选规则

**时间窗口:** 仅保留过去 24 小时内发布的内容(含当天,排除昨天已推过的)。

**日期锚定(必须执行):**
在抓取任何内容前,先运行以下命令获取今天的准确日期:
```bash
date +%Y-%m-%d
```
将输出结果作为 `TODAY` 变量,后续所有时间判断以此为基准。
- 每篇文章必须找到明确的发布时间戳,**无法确认日期的文章直接跳过**
- 发布年份 ≠ `TODAY` 年份的文章**强制丢弃**,无论内容多相关
- 发布日期早于 `TODAY - 1天` 的文章**强制丢弃**

**优先级排序:**
1. 🔥 重大模型发布(GPT、Claude、Gemini、国产大模型新版本)
2. 🔥 突破性论文(被广泛讨论,而非普通 arXiv 预印本)
3. 👀 重要产品更新(影响开发者或普通用户的功能)
4. 👀 行业重大动态(融资、收购、政策)
5. 📌 其他有意思的科技消息

**必须过滤掉:**
- 标题党("震惊!""颠覆!""碾压")
- 纯营销稿、厂商软文
- 同一事件的重复报道(只保留最权威一家)
- 纯观点文章、无新事实的评论
- 炒作性质的"AI 要取代 XX 职业"类内容

---

## 输出格式

用 Markdown 格式生成,符合 Slack Block Kit 格式,总长度控制在 **2000 字以内**(Slack 不限制屏幕)。

结构如下:

```markdown
# 📰 今日科技简报 (YYYY-MM-DD)

## 🔥 必读 (最多 3 条)

### 1. [标题]
**一句话摘要**(30字内)

具体说明(50字内,交代 who/what/why)

🔗 [原文链接](URL) · 来源:xxx

---

### 2. ...

## 👀 值得看 (最多 4 条)

### 1. [标题]
摘要(50字内)
🔗 [链接](URL) · 来源:xxx

---

## 📌 简讯 (最多 5 条,仅标题+链接)

- [标题1](URL) · 来源
- [标题2](URL) · 来源
- ...

---

_本简报由 Claude Code Routine 自动生成,如需调整偏好请修改 skill 文件_
```

**格式要点:**
- 所有内容必须中文,英文标题需翻译(可保留原文在括号里)
- 摘要要有信息量,别写"某某公司发布新模型,详情见原文"这种废话
- 数字、模型名、产品名用英文原文保留(如 GPT-5、Claude 4.7)
- 如果 24 小时内真的没有值得推的内容,直接推 "今日无重点新闻,保持关注" 即可,不要硬凑
- Slack 消息使用 Block Kit 富文本格式,支持链接、加粗、代码块等

---

## 去重机制

**读取历史记录:**
每次运行前,先读取 repo 根目录的 `briefing_history.json`,获取过去 7 天推送过的标题/URL 列表。

**筛选时去重:**
丢弃标题高度相似或 URL 相同的条目。

**运行后更新:**
把本次推送的所有条目(标题+URL+日期)追加写入 `briefing_history.json`,保留最近 7 天。

**文件格式示例:**
```json
{
  "history": [
    {
      "date": "2026-04-22",
      "items": [
        {"title": "xxx", "url": "https://..."}
      ]
    }
  ]
}
```

---

## 推送步骤

生成好内容后，通过 **Slack MCP 工具**（`mcp__Slack__slack_send_message`）推送。

### 推送方式：Slack MCP 工具（唯一推荐方式）

> ⚠️ **重要**：沙箱网络环境会阻止直接访问 `hooks.slack.com`（返回 403 host_not_allowed）。
> 必须使用 Claude Code 原生 MCP 工具 `mcp__Slack__slack_send_message`，不要使用 curl / webhook URL。

**目标频道（DM）：** `U0AUJKFLAKE`（当前登录用户）

**推送规则：**
- 消息中**不能使用** `---` 水平分隔线（会导致 invalid_blocks 错误）
- 链接直接写 URL，不用 `<url|text>` 格式
- 分两条消息发送，第二条以 thread_ts 回复第一条，保持会话整洁

**第一条消息（必读）：**
```
📰 **今日科技简报 (YYYY-MM-DD)**

🔥 **必读（N条）**

**1. [标题]**
[摘要50字内]
来源: [媒体名] [URL]

**2. [标题]**
...
```

**第二条消息（值得看 + 简讯，回复第一条）：**
```
👀 **值得看（N条）**

**1. [标题]**
[摘要]
来源: [媒体名] [URL]

📌 **简讯（N条）**

- [标题] · [媒体名] [URL]
- ...

_本简报由 Claude Code Routine 自动生成 · 共 N 条新闻_
```

**推送流程（伪代码）：**
```
1. 调用 mcp__Slack__slack_send_message(channel_id="U0AUJKFLAKE", message=必读内容)
   → 取返回的 message_ts

2. 调用 mcp__Slack__slack_send_message(
     channel_id="D0AUTUJARK3",   # 与 U0AUJKFLAKE 的 DM 频道 ID
     thread_ts=上一步的 message_ts,
     message=值得看+简讯内容
   )
```

---

## 异常处理

- **所有信息源都访问失败:** 用 `mcp__Slack__slack_send_message` 推送"今日新闻抓取失败,请检查网络或源站可用性"
- **MCP 推送失败:** 把内容保存到 repo 的 `last_failed.md`,方便下次运行时重试或人工查看
- **内容为空:** 推送"今日无重点新闻,保持关注"

---

## 执行流程总结

1. 运行 `date +%Y-%m-%d` 获取今天日期,记为 `TODAY`
2. 读取 `briefing_history.json` 获取近 7 天已推送列表
3. 按优先级遍历信息源,抓取过去 24 小时内容(严格以 `TODAY` 为基准过滤年份和日期)
4. 应用筛选规则 + 去重
5. 按"必读 / 值得看 / 简讯"三档组织内容
6. 生成中文 Markdown
7. **通过 `mcp__Slack__slack_send_message` 推送到 Slack**（分两条消息，第二条线程回复）
8. 更新 `briefing_history.json`
9. git commit + push
10. 输出本次推送标题列表到日志

