---
name: daily-tech-briefing
description: 每日 LLM 与科技新闻简报,抓取、筛选、整理成中文摘要并通过 Server 酱推送到微信
---

# 每日 LLM 与科技新闻简报

## 任务目标

每天早上生成一份简洁的中文科技新闻简报,通过 Server 酱推送到微信。
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

用 Markdown 格式生成,总长度控制在 **800 字以内**(微信一屏可看完)。

结构如下:

```
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

生成好 Markdown 内容后,通过 Server 酱推送。

**API 格式:**
```
POST https://sctapi.ftqq.com/<SENDKEY>.send
Content-Type: application/x-www-form-urlencoded

title=今日科技简报
desp=<Markdown 内容,需 URL encode>
```

**SENDKEY 从 repo 的环境变量 `SERVERCHAN_SENDKEY` 读取**(在 Routine 的 secrets 配置里设置,不要硬编码)。

**bash 推送命令:**
```bash
curl -X POST "https://sctapi.ftqq.com/${SERVERCHAN_SENDKEY}.send" \
  --data-urlencode "title=📰 今日科技简报 $(date +%m-%d)" \
  --data-urlencode "desp=${BRIEFING_CONTENT}"
```

**推送后检查返回:**
- `{"code":0}` 成功
- 其他 code 说明失败,记录日志,必要时重试 1 次

**额度提醒:**
Server 酱免费版每天 5 条上限,本任务每天 1 次推送,剩余 4 条作为故障重试或调试用。
相同内容 5 分钟内不能重复发送,不同内容一分钟只能发送 30 条(本任务不会触发)。

---

## 异常处理

- **所有信息源都访问失败:** 推送一条"今日新闻抓取失败,请检查网络或源站可用性"到微信,并退出
- **Server 酱推送失败:** 把内容保存到 repo 的 `last_failed.md`,方便下次运行时重试或人工查看
- **内容为空:** 推送"今日无重点新闻"
- **超过 Server 酱当日推送配额:** 记录日志,不重试(免费版每天 5 条上限)

---

## 执行流程总结

1. 读取 `briefing_history.json` 获取近 7 天已推送列表
2. 按优先级遍历信息源,抓取过去 24 小时内容
3. 应用筛选规则 + 去重
4. 按"必读 / 值得看 / 简讯"三档组织内容
5. 生成中文 Markdown
6. 通过 Server 酱推送
7. 更新 `briefing_history.json`
8. 输出本次推送摘要到 Routine 日志
