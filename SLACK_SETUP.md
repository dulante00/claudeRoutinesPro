# Slack 通知配置指南

## 🎯 概述

项目已更新为使用 Slack Webhook 推送每日科技简报。

相比微信推送的优点：
- ✅ 官方 API 支持，更稳定
- ✅ 企业级服务，可靠性高
- ✅ 支持富文本格式（Markdown）
- ✅ 支持线程回复、表情反应等交互
- ✅ 完整的消息历史

---

## 📋 快速设置（5分钟）

### 步骤1️⃣：在 Slack 中创建 Incoming Webhook

1. **打开 Slack Workspace**
   - 前往：https://api.slack.com/apps
   
2. **创建新应用**
   - 点击 "Create New App"
   - 选择 "From scratch"
   - App Name: `科技简报机器人`
   - Pick a workspace: 选择你的 Workspace
   - 点击 "Create App"

3. **启用 Webhook**
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
   - 保管好这个 URL，稍后会用到

### 步骤2️⃣：在 GitHub 中添加 Secret

1. **打开 GitHub 仓库设置**
   ```
   https://github.com/dulante00/claudeRoutinesPro/settings
   ```

2. **添加 Secret**
   - Security → Secrets and variables → Actions
   - 点击 "New repository secret"
   - Name: `SLACK_WEBHOOK_URL`
   - Value: 粘贴上面复制的 Webhook URL
   - 点击 "Add secret"

### 步骤3️⃣：测试工作流

1. **打开 Actions 标签**
   ```
   https://github.com/dulante00/claudeRoutinesPro/actions
   ```

2. **运行工作流**
   - 选择 "📰 每日科技简报"
   - 点击 "Run workflow"
   - 选择分支：`claude/eager-newton-k7jil`（或 `main` 如果已合并）
   - 点击 "Run workflow"

3. **验证**
   - 等待 2-3 分钟
   - 查看工作流日志（绿色 ✅ 表示成功）
   - 检查 Slack 频道，应该能看到消息

---

## 📊 Slack 消息格式

推送的消息包含：

```
📰 今日科技简报 (2026-04-22)

## 🔥 必读
### 1. Claude 3.5 Sonnet 发布
**Anthropic 推出最新版 Claude 3.5 Sonnet 模型，性能大幅提升**
...

## 👀 值得看
...

## 📌 简讯
...

_生成于 2026-04-22 · Claude Code Routine_
```

---

## 🔧 配置说明

### 环境变量

工作流使用的环境变量：
```yaml
SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
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

## ❓ 常见问题

**Q: Webhook URL 能公开吗？**
A: 不能！这个 URL 可以用来向频道发送消息。应该作为 Secret 保管。

**Q: 如何改变推送频道？**
A: 重新创建一个新的 Webhook，指向不同的频道，然后更新 Secret。

**Q: 如何禁用推送？**
A: 删除 Slack 的 Webhook，或从 GitHub Secrets 中删除环保变量。

**Q: 错过了推送如何补救？**
A: 在 Actions 中手动触发工作流重新推送。

**Q: 如何自定义消息格式？**
A: 编辑 `daily_briefing.py` 中的 `push_to_slack()` 方法，修改 `slack_message` 的结构。

---

## 🔐 安全提示

✅ **Secret 管理**
- Webhook URL 仅存储在 GitHub Secrets
- 不会在日志或代码中显示
- 定期轮换 Webhook URL（在 Slack 管理界面）

✅ **权限控制**
- Webhook 只能向指定频道发送消息
- 不能访问其他频道或用户信息
- Slack 限制了 Webhook 的权限

---

## 📚 相关文档

- [Slack API 文档](https://api.slack.com/messaging/webhooks)
- [Block Kit Builder](https://app.slack.com/block-kit)（消息格式设计工具）

---

## ✨ 下一步

现在你已经可以：
- ✅ 每天自动推送简报到 Slack
- ✅ 在任何时间手动触发推送
- ✅ 查看完整的执行日志

Happy automating! 🚀
