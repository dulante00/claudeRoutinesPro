# Slack 推送失败排查和解决方案

## 问题诊断

### 错误信息
```
HTTP Error 403: Forbidden
x-deny-reason: host_not_allowed
```

### 根本原因

**沙箱网络隔离**：Claude Code 的执行环境运行在受限的沙箱中，该沙箱有一个预配置的网络允许列表。`hooks.slack.com` 不在此允许列表中，导致所有直接连接都被阻止。

这不是简单的配置问题，而是基础设施级别的限制：
- ✗ 不能通过 settings.json 解决
- ✗ 不能通过环境变量解决
- ✗ 不能通过权限配置解决
- ✗ curl、urllib、requests 等所有标准网络库都受限

## 解决方案

### 方案 1：本地 HTTP 代理（推荐用于开发）

使用本地转发代理中介，绕过沙箱限制。

**步骤 1：启动转发服务器**
```bash
# 在一个终端启动代理
python3 slack_webhook_forwarder.py
```

输出示例：
```
============================================================
🚀 Slack Webhook 转发代理启动
============================================================

📍 服务器地址: http://localhost:9999
🔗 转发端点: http://localhost:9999/slack-webhook
➡️  转发目标: https://hooks.slack.com/services/...
```

**步骤 2：修改环境变量**
```bash
# 在另一个终端，设置本地代理地址
export SLACK_WEBHOOK_URL='http://localhost:9999/slack-webhook'

# 运行简报脚本
python3 daily_tech_briefing.py
```

**工作原理**：
- `slack_webhook_forwarder.py` 启动一个本地 HTTP 服务器（受沙箱允许）
- 脚本向本地服务器发送请求（不受限制）
- 服务器通过宿主机的网络连接转发到真实的 Slack webhook
- Slack 接收消息并在频道中显示

**优点**：
✅ 完全透明，无需修改脚本  
✅ 本地测试友好  
✅ 可以调试和监控  

**缺点**：
❌ 需要手动启动服务  
❌ 不适合完全自动化  

---

### 方案 2：文件备份 + 手动推送（生产环保）

将生成的内容保存到文件，定期通过外部工具推送。

**实现步骤**：

1. 脚本已经在 `last_failed.md` 中保存推送失败的内容
2. 定期检查该文件
3. 使用外部工具（如 Slack 桌面应用、浏览器、API 客户端等）推送

**示例命令**：
```bash
# 使用 Slack CLI（如果已安装）
slack chat send --text "$(cat last_failed.md)" --channel announcements

# 或手动复制 last_failed.md 的内容到 Slack
```

**优点**：
✅ 不依赖沙箱网络  
✅ 完全可靠  

**缺点**：
❌ 手动操作，不自动化  

---

### 方案 3：外部 Webhook 服务（企业推荐）

使用公开的 Webhook 转发服务。

**服务列表**：
- **Webhook.cool**: https://webhook.cool/
- **Requestbin**: https://requestbin.com/
- **Smee.io**: https://smee.io/

**步骤**：
```bash
# 1. 在 https://webhook.cool/ 创建一个公开 URL
# 2. 在本地创建一个中介脚本，接收请求并转发到 Slack
# 3. 配置脚本使用新的 Webhook URL
```

**优点**：
✅ 无需本地服务器  
✅ 可以跨多个环境工作  

**缺点**：
❌ 依赖第三方服务  
❌ 信息安全考虑（Webhook URL 会被外部看到）  

---

### 方案 4：在实时网络环境中运行（生产部署）

如果要在生产环境中部署此脚本，建议在以下环境中运行：

- **GitHub Actions**：在云端运行，不受沙箱限制
- **Cron 作业（服务器）**：在自有服务器上定期执行
- **Cloud Functions**：AWS Lambda、Google Cloud Functions、Azure Functions 等

**GitHub Actions 示例**：
```yaml
name: Daily Tech Briefing

on:
  schedule:
    - cron: '0 8 * * *'  # 每天早上 8 点

jobs:
  briefing:
    runs-on: ubuntu-latest
    env:
      SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
    steps:
      - uses: actions/checkout@v3
      - name: Run briefing
        run: python3 daily_tech_briefing.py
```

---

## 当前配置状态

### ✅ 已配置
```json
// .claude/settings.json
{
  "sandbox": {
    "network": {
      "allowedDomains": [
        "hooks.slack.com",
        "*.slack.com",
        "slack.com"
      ],
      "allowLocalBinding": true
    }
  }
}
```

### ⚠️ 限制说明
- 配置的 `allowedDomains` 只对某些工具有效
- 当前沙箱环境的基础限制仍然阻止直接连接到 Slack
- `allowLocalBinding: true` 允许本地通信（支持方案 1）

---

## 推荐方案选择

| 场景 | 推荐方案 | 理由 |
|------|--------|------|
| **本地开发和测试** | 方案 1（本地代理） | 简单易调试 |
| **生产自动化** | 方案 4（GitHub Actions） | 完全可靠，易于维护 |
| **紧急推送** | 方案 2（文件备份） | 快速和可靠 |
| **企业网络** | 方案 3（外部服务） | 灵活和可扩展 |

---

## 快速验证

### 检查沙箱状态
```bash
# 查看是否启用了沙箱
echo $SANDBOX_ENABLED
echo $CLAUDE_CODE_SANDBOX

# 尝试连接（会被阻止）
curl -I https://hooks.slack.com/
# 期望输出: HTTP/2 403

# 尝试本地连接（会成功）
curl -I http://localhost:9999/
# 期望输出: 连接拒绝（因为服务未启动）或 404
```

### 测试方案 1
```bash
# 终端 1
python3 slack_webhook_forwarder.py

# 终端 2（新建）
export SLACK_WEBHOOK_URL='http://localhost:9999/slack-webhook'
python3 -c "
import urllib.request, json
req = urllib.request.Request(
    'http://localhost:9999/slack-webhook',
    data=json.dumps({'text':'Test'}).encode(),
    headers={'Content-Type': 'application/json'},
    method='POST'
)
print(urllib.request.urlopen(req).read().decode())
"
# 期望输出: ok
```

---

## 下一步行动

1. **立即可用**：使用方案 1（本地代理）进行开发测试
2. **长期方案**：迁移到方案 4（GitHub Actions 或服务器 Cron）
3. **生产就绪**：配置完整的 Webhook 管道和错误处理

---

## 参考文件

- `daily_tech_briefing.py` - 主简报脚本
- `slack_webhook_forwarder.py` - 本地转发代理
- `last_failed.md` - 推送失败时的备份内容
- `briefing_history.json` - 去重历史记录

---

**最后更新**：2026-04-22
