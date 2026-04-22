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

生成好 Markdown 内容后,通过 Slack Connector 推送。

### 推送方式：Slack Connector（Claude Code 原生集成）

Slack Connector 是 Claude Code 提供的原生连接器，用于直接推送消息到 Slack。

**配置要求:**
1. 在 Slack Workspace 中创建 Incoming Webhook
2. 获取 Webhook URL: `https://hooks.slack.com/services/T.../B.../XXX`
3. 在 Claude Code 中配置环境变量:
   ```bash
   export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
   ```

**推送代码逻辑:**
```python
import urllib.request
import json

def push_to_slack(webhook_url: str, content: str) -> bool:
    """通过 Slack Webhook 推送"""
    
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
                    "text": content  # Markdown 内容
                }
            }
        ]
    }
    
    # 通过 Slack Connector 推送
    data = json.dumps(slack_message).encode('utf-8')
    req = urllib.request.Request(
        webhook_url,
        data=data,
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    
    response = urllib.request.urlopen(req)
    return response.read().decode('utf-8') == 'ok'
```

**推送后检查返回:**
- 返回 `ok` 表示成功
- 其他返回值或异常表示失败,记录日志,必要时重试 1 次

**Slack 优势:**
- ✅ 无推送频率限制（不像 Server 酱每天 5 条）
- ✅ 支持富文本格式（Block Kit）
- ✅ 支持线程回复、表情反应
- ✅ 消息永久存档，支持搜索
- ✅ 无需额外的第三方服务（Slack 官方 API）

---

## 异常处理

- **所有信息源都访问失败:** 推送一条"今日新闻抓取失败,请检查网络或源站可用性"到 Slack,并退出
- **Slack 推送失败:** 把内容保存到 repo 的 `last_failed.md`,方便下次运行时重试或人工查看
- **内容为空:** 推送"今日无重点新闻,保持关注"
- **SLACK_WEBHOOK_URL 未设置:** 输出错误日志,提示配置缺失

---

## 执行流程总结

1. 运行 `date +%Y-%m-%d` 获取今天日期,记为 `TODAY`
2. 读取 `briefing_history.json` 获取近 7 天已推送列表
3. 按优先级遍历信息源,抓取过去 24 小时内容(严格以 `TODAY` 为基准过滤年份和日期)
3. 应用筛选规则 + 去重
4. 按"必读 / 值得看 / 简讯"三档组织内容
5. 生成中文 Markdown
6. 通过 Bash curl 命令推送到 Slack（使用环境变量 SLACK_WEBHOOK_URL）
7. 更新 `briefing_history.json`
8. 输出本次推送摘要到 Routine 日志

