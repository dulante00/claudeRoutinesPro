# 📱 Slack 通知配置 - Claude Code Routines 版

## 🎯 概述

每日科技简报运行在 Claude Code Routines 沙箱中，通过 Slack Webhook 推送通知。

**执行环境：**
- ✅ Claude Code Routines 沙箱
- ✅ 有网络权限（可访问 Slack API）
- ✅ 支持定期执行或手动运行

**通知方式：**
- ✅ Slack Webhook
- ✅ 富文本格式（Block Kit）
- ✅ 支持线程、表情等交互

---

## 📋 快速设置（5分钟）

### 步骤1️⃣：在 Slack 中创建 Incoming Webhook

1. **打开 Slack Apps**
   ```
   https://api.slack.com/apps
   ```

2. **创建新应用**
   - 点击 "Create New App"
   - 选择 "From scratch"
   - App Name: `科技简报机器人`
   - Pick a workspace: 选择你的 Workspace
   - 点击 "Create App"

3. **启用 Incoming Webhooks**
   - 左侧菜单 → "Incoming Webhooks"
   - 点击 "Activate Incoming Webhooks"（如未启用）

4. **添加新 Webhook**
   - 点击 "Add New Webhook to Workspace"
   - 选择通知的频道（如 #announcements 或 #tech-news）
   - 点击 "Allow"

5. **复制 Webhook URL**
   ```
   https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX
   ```

### 步骤2️⃣：在 Claude Code 中设置环境变量

在 Claude Code Routines 中运行：

```bash
# 设置环境变量
export SLACK_WEBHOOK_URL="<粘贴上面复制的URL>"

# 验证设置
echo $SLACK_WEBHOOK_URL
```

或者在 `.claude/settings.json` 中配置：

```json
{
  "env": {
    "SLACK_WEBHOOK_URL": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
  }
}
```

### 步骤3️⃣：运行简报

```bash
# 直接执行
python3 daily_briefing.py

# 或通过 Shell 脚本
bash run_daily_briefing.sh
```

### 步骤4️⃣：验证推送

- 查看 Python 脚本的输出日志
- 检查 Slack 频道，应该能看到消息
- 验证：`✅ 成功推送到 Slack`

---

## 📊 Slack 消息格式

推送的消息包含：

```
📰 今日科技简报 (2026-04-22)

## 🔥 必读
### 1. Claude 3.5 Sonnet 发布
**Anthropic 推出最新版 Claude 3.5 Sonnet 模型，性能大幅提升**

🔗 [Anthropic](https://www.anthropic.com/news)

---

### 2. OpenAI 发布 GPT-4 Turbo 更新
**新版本增加了更好的多模态能力和更长的上下文窗口**

🔗 [OpenAI](https://openai.com/blog)

---

## 👀 值得看
...

## 📌 简讯
...

_生成于 2026-04-22 · Claude Code Routine_
```

---

## 🔧 配置说明

### 环境变量

脚本读取的环境变量：
```python
webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
```

### 推送逻辑

`daily_briefing.py` 中的推送代码：
```python
def push_to_slack(self, content: str) -> bool:
    """推送到 Slack"""
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    
    slack_message = {
        "text": title,
        "blocks": [
            {"type": "header", ...},
            {"type": "section", ...},
            {"type": "context", ...}
        ]
    }
    
    # 发送到 Slack API
    urllib.request.urlopen(webhook_url, data=json.dumps(slack_message))
```

---

## 📅 定期执行（可选）

### 方式1：Claude Code Hook（推荐）

在 `.claude/settings.json` 中配置定期任务（每日08:00）：

```json
{
  "hooks": {
    "daily-briefing": {
      "schedule": "0 8 * * *",
      "command": "python3 daily_briefing.py"
    }
  }
}
```

### 方式2：使用 Claude Code `/loop` 命令

```bash
/loop 24h python3 daily_briefing.py
```

这会每24小时执行一次。

### 方式3：Linux Crontab

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天 08:00）
0 8 * * * cd /path/to/claudeRoutinesPro && python3 daily_briefing.py
```

---

## ❓ 常见问题

**Q: Webhook URL 能公开吗？**
A: 不能！应该作为环境变量或 Secret 保管。

**Q: 如何改变推送频道？**
A: 重新创建一个新的 Webhook，指向不同的频道，然后更新环境变量。

**Q: 如何禁用推送？**
A: 删除或注释掉环境变量，脚本会输出错误但不会崩溃。

**Q: 推送失败如何处理？**
A: 脚本会保存失败内容到 `last_failed.md`，下次可以重新推送。

**Q: 如何自定义消息格式？**
A: 编辑 `daily_briefing.py` 中的 `push_to_slack()` 方法，修改 `slack_message` 的结构。

**Q: 如何加入真实的新闻数据？**
A: 编辑 `create_sample_briefing()` 函数，或改进 `fetch_sources.py` 中的爬虫逻辑。

---

## 🔐 安全建议

✅ **不要在代码中硬编码 Webhook URL**
- 使用环境变量
- 使用 Claude Code settings
- 定期轮换 Webhook URL

✅ **保护 Webhook URL**
- 不要提交到 Git
- 不要在日志中显示
- 限制访问权限

✅ **Slack 权限**
- Webhook 只能向指定频道发送消息
- 不能访问其他频道或用户信息
- Slack 限制了 Webhook 的权限

---

## 🚀 下一步

1. **创建 Slack Webhook**
   - 按上面的步骤1-4 操作
   - 复制 Webhook URL

2. **配置环境变量**
   - 设置 `SLACK_WEBHOOK_URL`

3. **测试推送**
   - 运行 `python3 daily_briefing.py`
   - 检查 Slack 收到消息

4. **设置定期执行**（可选）
   - 配置 Hook 或 Crontab
   - 每天自动推送

---

## 📚 相关文档

- [Slack API 文档](https://api.slack.com/messaging/webhooks)
- [Block Kit Builder](https://app.slack.com/block-kit)（消息格式设计）

---

**Happy automating!** 🚀
