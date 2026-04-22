# 🚀 快速开始 - 5 分钟完成设置

## 在 GitHub 中添加 Secret

这是唯一需要在 GitHub Web 界面中手动执行的步骤。

### 步骤：

1. **打开仓库设置**
   ```
   https://github.com/dulante00/claudeRoutinesPro/settings
   ```

2. **导航到 Secrets**
   - 左侧菜单：`Security` → `Secrets and variables`
   - 点击 `Actions` 标签

3. **创建新 Secret**
   - 点击 `New repository secret` 按钮
   - **Name**: `SERVERCHAN_SENDKEY`
   - **Value**: `SCT340923TlJvjazLY1zVuVb22fM6qNDWN`
   - 点击 `Add secret`

✅ **完成！** Secret 应该出现在列表中（值被隐藏）

---

## 测试工作流

### 第一次手动测试：

1. **打开 Actions 标签**
   ```
   https://github.com/dulante00/claudeRoutinesPro/actions
   ```

2. **选择工作流**
   - 左侧找到 `📰 每日科技简报`
   - 点击打开

3. **运行工作流**
   - 点击 `Run workflow`
   - 选择分支：`claude/eager-newton-k7jil`
   - 再次点击 `Run workflow`

4. **监控执行**
   - 页面会显示正在运行的工作流
   - 等待 2-3 分钟完成
   - 所有步骤应该显示为绿色 ✅

### 验证成功：

- [ ] GitHub Actions 日志显示成功
- [ ] 微信收到推送消息
- [ ] 日志显示 "✅ 简报已成功生成并推送"

---

## 之后会怎样？

✅ **自动推送** - 每天 UTC 0:00（北京时间 08:00）自动执行

✅ **自动更新** - 历史记录 `briefing_history.json` 自动更新

✅ **手动触发** - 任何时候可以在 Actions 中手动运行

✅ **完整日志** - 所有执行记录都可在 Actions 中查看

---

## 常见问题

**Q: 测试失败了？**
A: 查看 Actions 中的详细日志，参考 `GITHUB_ACTIONS_SETUP.md` 的故障排除部分

**Q: Secret 添加后多久生效？**
A: 立即生效，下一次工作流运行会使用新 Secret

**Q: 如何改变推送时间？**
A: 编辑 `.github/workflows/daily-briefing.yml`，修改 `cron` 表达式

**Q: 需要保持本地运行吗？**
A: 不需要，GitHub Actions 完全独立运行

---

## 需要帮助？

📖 详细文档：`GITHUB_ACTIONS_SETUP.md`

该文档包含：
- 完整的设置步骤
- 时间配置说明  
- 工作流详解
- 监控和调试
- 常见问题解答
- 故障排除

---

**就这样！** 🎉

添加 Secret → 测试一次 → 完成！

后续每天都会自动推送简报到微信。
