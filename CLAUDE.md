# claudeRoutinesPro — 项目规则

## 分支策略

**每个 routine 使用固定分支名，不使用 harness 随机分配的分支。**

| Routine / Skill | 固定分支名 |
|---|---|
| daily-tech-briefing | `claude/daily-briefing` |

### 执行规则

1. 每次 routine 启动时，先切换到（或创建）上表对应的固定分支：
   ```bash
   git fetch origin
   git checkout claude/daily-briefing 2>/dev/null || git checkout -b claude/daily-briefing origin/main
   git pull origin claude/daily-briefing 2>/dev/null || true
   ```

2. 所有改动在该固定分支上完成并 push。

3. **成功且有实质改动（briefing_history.json 或 SKILL.md 发生变化）时，自动合并到 main：**
   ```bash
   git checkout main
   git pull origin main
   git merge claude/daily-briefing --no-ff -m "merge: daily-briefing $(date +%Y-%m-%d)"
   git push origin main
   git checkout claude/daily-briefing
   ```

4. 若合并冲突或 push 失败，保留分支现状，在日志中输出告警，不强制合并。

## 提交规范

- briefing_history.json 更新：`📰 更新 YYYY-MM-DD 科技简报`
- SKILL 优化：`improve <skill>: <具体改动>`
- 修复：`fix: <问题描述>`
