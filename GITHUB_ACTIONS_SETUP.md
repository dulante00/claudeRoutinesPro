# GitHub Actions 自动推送指南

## 📋 概述

本指南将帮助你设置 GitHub Actions，使每日科技简报能够自动推送到微信。

**优势：**
- ✅ 自动化推送，无需手动干预
- ✅ 定时执行（每天早上8点）
- ✅ 自动提交历史记录更新
- ✅ 完整的日志和错误追踪
- ✅ 可手动触发
- ✅ 无需本地网络权限

---

## 🔧 操作步骤

### 第一步：配置 GitHub Secrets

这一步用于保存你的 Server 酱密钥，使工作流能够推送到微信。

**方式A：通过 GitHub Web 界面（推荐）**

1. 打开你的仓库：`https://github.com/dulante00/claudeRoutinesPro`

2. 进入 **Settings** → **Secrets and variables** → **Actions**

3. 点击 **New repository secret**

4. 填写以下信息：
   - **Name:** `SERVERCHAN_SENDKEY`
   - **Secret:** 粘贴你的 Server 酱密钥（`SCT340923TlJvjazLY1zVuVb22fM6qNDWN`）

5. 点击 **Add secret**

**验证：** Secret 添加后应该显示在列表中（值被隐藏）

---

### 第二步：验证工作流文件

工作流文件已经创建在 `.github/workflows/daily-briefing.yml`

**检查文件内容：**
```bash
cat .github/workflows/daily-briefing.yml
```

**文件应该包含：**
- 每天 UTC 0:00（北京时间 08:00）执行
- 调用 `python3 daily_briefing.py`
- 环境变量传递：`SERVERCHAN_SENDKEY`
- 自动提交历史记录更新

---

### 第三步：提交并推送到 GitHub

```bash
# 添加工作流文件
git add .github/workflows/daily-briefing.yml GITHUB_ACTIONS_SETUP.md

# 提交
git commit -m "feat: 添加GitHub Actions自动推送工作流

- 添加 .github/workflows/daily-briefing.yml
- 配置每日自动推送到微信
- 自动更新历史记录
- 支持手动触发

通过GitHub Actions在有网络权限的环境中完成推送。

https://claude.ai/code/session_01VrjoXetRfGQbyQGqDz6Rb7
"

# 推送到远程
git push -u origin claude/eager-newton-k7jil
```

---

### 第四步：创建 Pull Request（可选但推荐）

1. 前往 GitHub 仓库
2. 应该会看到"Compare & pull request"按钮
3. 点击创建 PR
4. 标题：`feat: 添加GitHub Actions自动推送`
5. 合并到 `main` 或 `master` 分支

---

### 第五步：测试工作流

**方式1：等待定时执行**
- 工作流每天 UTC 0:00（北京时间 08:00）自动运行
- 查看：**Actions** 标签页

**方式2：立即测试（推荐）**

1. 进入仓库 → **Actions** 标签
2. 左侧选择 **📰 每日科技简报**
3. 点击 **Run workflow**
4. 选择 **Branch:** `claude/eager-newton-k7jil`
5. 点击 **Run workflow**

**监控执行：**
- 工作流会立即开始执行
- 可以看到实时日志：
  - 📥 检出代码
  - 🐍 设置Python环境
  - 🚀 生成并推送简报
  - 💾 提交历史记录

---

## 📊 工作流详解

### 工作流内容

```yaml
name: 📰 每日科技简报

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 00:00 执行
  workflow_dispatch:     # 手动触发

jobs:
  briefing:
    runs-on: ubuntu-latest
    
    steps:
      1. 检出代码（git checkout）
      2. 设置Python 3.11环境
      3. 运行 daily_briefing.py
      4. 自动提交历史记录更新
      5. 错误处理和日志输出
```

### 时间配置

Cron 表达式：`0 0 * * *`

| 字段 | 含义 | 当前值 |
|------|------|--------|
| 分钟 | 0-59 | 0 |
| 小时 | 0-23 | 0（UTC） |
| 天 | 1-31 | *（每天） |
| 月 | 1-12 | *（每月） |
| 周几 | 0-6 | *（每天） |

**转换到北京时间（UTC+8）：**
- UTC 0:00 = 北京时间 08:00

**改时间的例子：**
- 下午3点（北京时间）= UTC 07:00 → `0 7 * * *`
- 晚上9点（北京时间）= UTC 13:00 → `0 13 * * *`

---

## 🔍 监控和调试

### 查看工作流日志

1. 进入仓库 → **Actions** 标签
2. 选择最近的运行记录
3. 查看详细日志：
   - 绿色 ✅ = 成功
   - 红色 ❌ = 失败
   - 黄色 ⚠️ = 警告

### 常见问题

**问题1：Secret 未找到**
```
Error: SERVERCHAN_SENDKEY not found
```
**解决：** 重新确认 Secret 已添加，名称完全匹配

**问题2：推送失败**
```
HTTP 403: Host not in allowlist
```
**原因：** GitHub Actions 也可能在某个网络策略下被拒绝
**解决：** 更换 GitHub 账户或联系企业IT

**问题3：权限不足**
```
fatal: Permission denied (publickey)
```
**原因：** GitHub 认证问题
**解决：** 仓库需要 push 权限

### 查看执行记录

```bash
# 也可以本地查看推送历史
git log --oneline | grep -i "briefing\|chore"
```

---

## 📝 自定义配置

### 改变执行时间

编辑 `.github/workflows/daily-briefing.yml`：

```yaml
schedule:
  - cron: '0 8 * * *'  # 改成北京时间 16:00
```

### 改变推送内容

编辑 `daily_briefing.py` 中的 `create_sample_briefing()` 函数

### 添加新的信息源

编辑 `fetch_sources.py`，添加新的 NewsSource 子类

---

## ✅ 验证清单

- [ ] SERVERCHAN_SENDKEY Secret 已添加
- [ ] `.github/workflows/daily-briefing.yml` 文件存在
- [ ] 代码已推送到远程分支
- [ ] 在 GitHub Actions 中手动触发了一次测试
- [ ] 测试运行成功（绿色 ✅）
- [ ] 微信收到了推送消息
- [ ] 历史记录文件已更新

---

## 🚀 下一步

1. **监控首次运行**
   - 手动触发工作流
   - 检查是否成功推送到微信

2. **设置定时任务**
   - 工作流每天自动运行
   - 无需手动干预

3. **持续改进**
   - 实现真实的新闻源爬取
   - 改进筛选和分类逻辑
   - 添加更多信息源

---

## 📞 故障排除

如果工作流失败：

1. 查看 **Actions** 标签的日志
2. 检查 Secret 配置
3. 确认网络可访问 Server 酱
4. 查看 `last_failed.md` 中保存的内容

---

## 💡 其他资源

- [GitHub Actions 文档](https://docs.github.com/en/actions)
- [Cron 时间表生成器](https://crontab.guru/)
- [Server 酱文档](https://sct.ftqq.com/)

---

**祝你推送顺利！** 🎉
