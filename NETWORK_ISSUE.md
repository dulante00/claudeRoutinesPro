# 网络爬虫访问问题诊断

## 问题现象
```
HTTP Error 403: Host not in allowlist
```

## 根本原因
当前环境实施了网络访问策略：
- ✗ 外网主机 (Google, Slack hooks, 新闻网站 等) 被阻止
- ✗ 过滤规则：`host_not_allowed`
- ✓ 本地 MCP 工具（Slack 集成）可用
- ✓ 内部网络服务（Git）可用

## 解决方案

### 方案 1：白名单所需主机（推荐）
在网络策略中为爬虫添加以下域名白名单：

**一级源（必需）：**
- `www.jiqizhixin.com` (机器之心)
- `www.qbitai.com` (量子位)
- `www.anthropic.com` (Anthropic)
- `openai.com` (OpenAI)

**二级源（可选）：**
- `36kr.com` (36氪)
- `infoq.cn` (InfoQ)
- `sspai.com` (少数派)
- `news.ycombinator.com` (Hacker News)
- `arxiv.org` (arXiv 论文)

### 方案 2：使用本地爬虫驱动
通过 Puppeteer/Playwright 在本地运行浏览器自动化爬虫（需安装额外依赖）

### 方案 3：使用新闻 API
接入第三方 API 服务（如 NewsAPI, Diffbot）获取结构化数据

## 当前状态
- ✅ 脚本功能完整（爬虫、筛选、去重、推送）
- ✅ 通过示例数据成功演示全流程
- ✅ Slack 集成验证通过
- ⏸️ 实时网页爬虫受限于网络策略

## 建议
请管理员在网络策略中添加上述新闻源的白名单，即可启用实时爬虫功能。
