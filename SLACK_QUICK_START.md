# 📰 日科技简报 - Slack 推送使用指南

## 🎯 概述

**执行环境:** Claude Code Routines 沙箱
**推送方式:** Slack Connector（原生集成）
**内容:** LLM 与科技新闻简报

---

## ⚡ 5分钟快速开始

### 步骤1️⃣：创建 Slack Webhook

1. 打开 https://api.slack.com/apps
2. 创建新应用：From scratch
3. 应用名称：`科技简报机器人`
4. 选择你的 Workspace
5. 左侧菜单 → Incoming Webhooks → Activate
6. Add New Webhook to Workspace
7. 选择频道（如 #announcements）
8. 复制 Webhook URL

### 步骤2️⃣：设置环境变量

```bash
export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/T.../B.../XXX"
```

或在 `.claude/settings.json` 中：

```json
{
  "env": {
    "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/..."
  }
}
```

### 步骤3️⃣：执行简报

```bash
python3 daily_briefing.py
```

### 步骤4️⃣：验证

- 查看日志输出：`✅ 成功推送到 Slack`
- 检查 Slack 频道：应该能看到简报消息

---

## 📅 定期执行设置

### 方式1️⃣：Claude Code Hook（推荐）

编辑 `.claude/settings.json`：

```json
{
  "hooks": {
    "daily-briefing": {
      "schedule": "0 8 * * *",
      "command": "cd /path/to/claudeRoutinesPro && python3 daily_briefing.py"
    }
  }
}
```

**时间说明：**
- `0 8 * * *` = 每天 08:00 UTC（可改为你需要的时间）
- 北京时间：`0 0 * * *` = 每天 08:00

### 方式2️⃣：/loop 命令（快速）

```bash
/loop 24h python3 daily_briefing.py
```

### 方式3️⃣：Crontab（系统级）

```bash
crontab -e

# 添加这一行
0 8 * * * cd /home/user/claudeRoutinesPro && python3 daily_briefing.py
```

---

## 📊 功能特性

### ✅ 新闻抓取与筛选
- 🔥 重大模型发布（GPT、Claude、Gemini 等）
- 🔥 突破性论文（被广泛讨论的重要研究）
- 👀 重要产品更新（影响开发者或用户的功能）
- 👀 行业重大动态（融资、收购、政策）
- 📌 其他有意思的科技消息

### ✅ 自动去重
- 基于 URL 的精确去重
- 基于标题相似度的智能去重
- 保留 7 天历史记录

### ✅ Slack 推送优势
- 📨 无推送频率限制（不像 Server 酱每天 5 条）
- 📝 支持富文本格式（Block Kit）
- 💬 支持线程、表情等交互
- 🔍 消息永久存档，支持搜索
- 🚀 无需第三方依赖，Slack 官方 API

---

## 📝 输出示例

```
📰 今日科技简报 (2026-04-22)

🔥 必读
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Claude 3.5 Sonnet 发布
**Anthropic 推出最新版本，性能大幅提升**

新版本支持 200K token 上下文窗口，推理速度提升 40%。
🔗 [Anthropic](https://anthropic.com) · 来源: Anthropic

2. OpenAI 发布 GPT-4 Turbo 更新
**增加多模态能力和上下文窗口**

...

👀 值得看
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
...

📌 简讯
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- [谷歌 Gemini 新版本](https://google.com) · 量子位
- [Meta 开源新模型](https://meta.com) · 36氪
```

---

## 🔧 配置参考

### 环境变量
```bash
# 必需
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# 可选
SLACK_CHANNEL=#tech-news  # 指定频道
```

### 推送内容
- 📏 Markdown 格式，最多 2000 字
- 🎨 自动转换为 Slack Block Kit
- 🔗 包含原文链接和来源信息

### 历史记录
- 📄 `briefing_history.json` - 自动去重
- 📅 保留 7 天记录
- 🔄 每次推送后自动更新

---

## ❓ 常见问题

**Q: Webhook URL 丢失了怎么办？**
A: 在 Slack 管理界面重新生成一个新的 Webhook。

**Q: 推送失败了怎么办？**
A: 内容会保存到 `last_failed.md`，查看日志找原因。

**Q: 如何改变推送频道？**
A: 创建新的 Webhook 指向不同频道，更新 `SLACK_WEBHOOK_URL`。

**Q: 如何自定义消息格式？**
A: 编辑 `daily_briefing.py` 中的 `push_to_slack()` 方法。

**Q: 如何加入真实的新闻数据？**
A: 改进 `fetch_sources.py` 中的爬虫逻辑或集成新闻 API。

**Q: 是否支持多个频道推送？**
A: 当前支持单个频道。可通过修改代码支持多频道。

---

## 📚 相关文件

- `.claude/skills/daily-tech-briefing/SKILL.md` - 完整的 skill 定义
- `daily_briefing.py` - 简报生成和推送脚本
- `fetch_sources.py` - 新闻源爬虫（可选扩展）
- `briefing_history.json` - 历史记录和去重数据
- `SLACK_SETUP.md` - 详细的 Slack 配置指南

---

## 🚀 下一步

1. ✅ 创建 Slack Webhook
2. ✅ 设置 `SLACK_WEBHOOK_URL` 环境变量
3. ✅ 运行 `python3 daily_briefing.py` 测试
4. ✅ 配置定期执行（选择上面的方式1、2或3）
5. ✅ 验证 Slack 收到消息

---

**祝你使用愉快！** 🎉

有问题？参考 `SLACK_SETUP.md` 获取更多详细信息。
