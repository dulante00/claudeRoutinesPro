# 分支管理和部署指南

## 📍 当前分支结构

```
GitHub 仓库
├── main（主分支 - 生产代码）
│   └─ 目前没有 daily_briefing 工作流
│   └─ 可能是其他稳定功能
│
└── claude/eager-newton-k7jil（开发分支）
    └─ ✅ 包含完整的 daily_briefing 实现
    └─ ✅ 包含 GitHub Actions 工作流
    └─ ✅ 包含所有配置和文档
    └─ 每次执行都使用这个分支的代码
```

---

## 🔄 GitHub Actions 工作流执行流程

### 当前情况

```
┌─────────────────────────────────────┐
│  GitHub Actions 触发                │
│  (定时：每天 UTC 0:00)             │
│  (手动：Run workflow)               │
└────────────────┬────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────┐
│  检出代码                            │
│  uses: actions/checkout@v4          │
│                                     │
│  ✅ 检出的是：                      │
│     - 当前分支的代码                │
│     - 即 claude/eager-newton-k7jil │
└────────────────┬────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────┐
│  执行脚本                            │
│  python3 daily_briefing.py          │
│                                     │
│  使用的文件：                        │
│  - daily_briefing.py                │
│  - briefing_history.json            │
│  - 等其他依赖                       │
└────────────────┬────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────┐
│  推送到 Slack                       │
│  使用：SLACK_WEBHOOK_URL            │
│  (来自 GitHub Secrets)              │
└─────────────────────────────────────┘
```

---

## ❓ "每次执行的代码是哪个分支的？"

### 答案：工作流文件所在的分支

当你在某个分支上创建或修改 `.github/workflows/` 中的文件时，GitHub Actions 会：

1. **找到工作流文件** → `.github/workflows/daily-briefing.yml`
2. **确定工作流所在的分支** → 该文件存在的分支
3. **使用该分支的代码执行** → 检出相同分支，运行工作流

### 当前配置

```yaml
name: 📰 每日科技简报

on:
  schedule:
    - cron: '0 0 * * *'  # 每天 UTC 0:00
  workflow_dispatch:     # 手动触发

# ⚠️ 注意：没有指定 branches: [main]
# 这意味着工作流会在包含它的分支上执行
```

---

## 📊 两种部署策略

### 策略 A：开发分支执行（当前）

✅ **优点**
- 开发和生产分离
- 可以在开发分支进行实验
- 不影响 main 分支

❌ **缺点**
- 需要单独维护两个分支
- 容易忘记合并
- 不清楚生产代码来自哪里

**使用场景**
- 还在测试和调试阶段
- 想保持 main 分支的干净

```
现在的情况：
work flow 文件存在于 → claude/eager-newton-k7jil
GitHub Actions 执行的代码 → claude/eager-newton-k7jil
main 分支 → 没有此功能
```

### 策略 B：合并到 main 执行（推荐）

✅ **优点**
- 统一管理，更清晰
- 生产代码来源明确
- 符合 Git Flow 标准
- 易于维护和回滚

❌ **缺点**
- main 分支代码需要稳定
- 不能随意实验

**使用场景**
- 功能已稳定
- 准备长期运维
- 多人协作项目

---

## 🚀 如何从策略 A 迁移到策略 B

### 第一步：在 main 分支上创建工作流

```bash
# 1. 切换到 main 分支
git checkout main

# 2. 从 claude/eager-newton-k7jil 拉取最新内容
git merge claude/eager-newton-k7jil

# 3. 验证文件存在
ls -la .github/workflows/daily-briefing.yml
ls -la daily_briefing.py

# 4. 推送到 GitHub
git push origin main
```

### 第二步：确保 Secret 已配置

GitHub Secrets 是仓库级别的，对所有分支都有效：
```
https://github.com/dulante00/claudeRoutinesPro/settings/secrets/actions
```

Secret 不需要重新配置，所有分支都可以访问：
- `SLACK_WEBHOOK_URL` ✅
- （之前的 `SERVERCHAN_SENDKEY` 可以删除）

### 第三步：测试从 main 执行

```bash
# 在 GitHub Actions 中：
1. 打开 Actions 标签
2. 选择工作流
3. 点击 "Run workflow"
4. 选择分支：main（而不是 claude/eager-newton-k7jil）
5. 点击 "Run workflow"
```

### 第四步：后续维护

之后的开发流程：
```
feature 分支
    ↓
创建 Pull Request 到 main
    ↓
代码审核
    ↓
合并到 main
    ↓
GitHub Actions 自动执行（使用 main 分支的代码）
```

---

## 📋 检查清单

### 当前状态（策略 A）

- [x] 工作流文件在 `claude/eager-newton-k7jil`
- [x] 代码也在 `claude/eager-newton-k7jil`
- [x] 每天自动执行（使用开发分支的代码）
- [x] `SLACK_WEBHOOK_URL` Secret 已配置
- [ ] main 分支没有此功能

### 迁移到策略 B（可选）

- [ ] 确保开发分支代码稳定
- [ ] 合并 `claude/eager-newton-k7jil` 到 `main`
- [ ] 验证 `.github/workflows/` 在 main 上
- [ ] 验证 `daily_briefing.py` 在 main 上
- [ ] 测试从 main 分支执行工作流
- [ ] 更新文档说明生产分支

---

## 🎯 建议

**短期（实验阶段）**
- 保持当前策略 A
- 在 `claude/eager-newton-k7jil` 上开发和测试
- 工作流已经正常执行

**长期（稳定运维）**
- 建议迁移到策略 B
- 合并到 main 作为生产代码
- 清晰的分支管理和部署流程

---

## 📚 相关文档

- [SLACK_SETUP.md](SLACK_SETUP.md) - Slack 配置指南
- [QUICK_START.md](QUICK_START.md) - 快速开始
- [GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md) - 完整配置指南

---

## 🔗 Git 命令参考

```bash
# 查看当前分支
git branch

# 查看所有分支（包括远程）
git branch -a

# 切换分支
git checkout main

# 合并分支到当前分支
git merge claude/eager-newton-k7jil

# 推送当前分支
git push origin

# 查看分支的提交历史
git log --graph --all --oneline
```

---

**需要帮助？参考本文件的相应章节。** 📖
